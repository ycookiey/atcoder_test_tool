import tkinter as tk
import os

from ui.theme_manager import ThemeManager
from ui.main_window import MainWindow
from core.html_manager import HTMLManager
from core.test_runner import TestRunner
from core.code_manager import CodeManager
from core.file_monitor import FileMonitor
from core.clipboard_monitor import ClipboardMonitor


class AtCoderTestTool:
    """AtCoderテストツールのメインクラス"""

    def __init__(self, root):
        self.root = root
        self.root.title("AtCoder Test Tool")
        self.root.geometry("1280x800")

        self.contest_number = ""
        self.problem_id = ""
        self.problem_title = ""

        self.problems = {}  # problem_id -> problem_info

        self.theme_manager = ThemeManager(root)

        self.html_manager = HTMLManager(self)
        self.test_runner = TestRunner(self)
        self.code_manager = CodeManager(self)

        self.ui = MainWindow(root, self)

        self.file_monitor = FileMonitor("", self.code_manager.reload_code_file)
        self.file_monitor.start()

        self.clipboard_monitor = ClipboardMonitor(self)
        self.clipboard_monitor.start()

    def activate_window(self):
        """アプリケーションウィンドウをアクティブにする"""
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.deiconify()
        self.root.focus_force()
        self.root.lift()
        self.root.attributes("-topmost", False)

        self.ui.show_status_message(
            "ウィンドウをアクティブにしました", "Success.TLabel"
        )

    def paste_from_clipboard(self):
        """クリップボードの内容をHTML入力欄に貼り付け"""
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content:
                self.ui.html_text.delete("1.0", tk.END)
                self.ui.html_text.insert(tk.END, clipboard_content)
                self.ui.show_status_message(
                    "クリップボードから貼り付けました", "Success.TLabel"
                )
                self.start_parsing()
        except Exception as e:
            self.ui.show_status_message(
                f"クリップボードからの貼り付けに失敗しました", "Error.TLabel"
            )

    def on_html_change(self, event=None):
        """HTMLテキストエリアの内容が変更されたらパースを実行"""
        html_content = self.ui.html_text.get("1.0", tk.END).strip()
        if len(html_content) > 100 and not self.html_manager.parsing:
            self.start_parsing()

    def on_tab_changed(self, event):
        """タブ変更時のイベントハンドラ"""
        current_tab = self.ui.notebook.index(self.ui.notebook.select())

        # HTML入力タブの場合
        if current_tab == 0:
            html_content = self.ui.html_text.get("1.0", tk.END).strip()
            if not html_content or len(html_content) < 100:
                pass
        # テストケースタブの場合
        elif current_tab == 1:
            html_content = self.ui.html_text.get("1.0", tk.END).strip()
            if not html_content or len(html_content) < 100:
                self.ui.notebook.select(0)
                self.ui.show_status_message("HTMLを入力してください", "Warning.TLabel")
        # 問題タブの場合
        else:
            tab_info = self.ui.get_current_tab_info()
            if tab_info and "problem_id" in tab_info:
                problem_id = tab_info["problem_id"]
                if problem_id in self.problems:
                    problem_info = self.problems[problem_id]
                    self.code_manager.update_code_file_path(
                        problem_info["contest_number"], problem_info["problem_id"]
                    )
                    if self.code_manager.code_file:
                        self.file_monitor.update_file_path(self.code_manager.code_file)

    def start_parsing(self):
        """HTML解析を開始"""
        html_content = self.ui.html_text.get("1.0", tk.END)
        self.html_manager.start_parsing(html_content)

    def update_problem_info(self, problem_info):
        """問題情報を更新"""
        self.problem_id = problem_info["problem_id"]
        self.problem_title = problem_info["problem_title"]
        self.contest_number = problem_info["contest_number"]

        problem_id = problem_info["problem_id"]
        self.problems[problem_id] = problem_info

        self.code_manager.set_current_problem_info(problem_info)

        if self.contest_number and self.problem_id and self.problem_title:
            info_text = (
                f"ABC {self.contest_number} - {self.problem_id}: {self.problem_title}"
            )
            self.ui.info_label.config(text=info_text)

            code_file = self.code_manager.update_code_file_path(
                self.contest_number, self.problem_id
            )

            if code_file:
                self.code_manager.update_code_frame(code_file)

                self.file_monitor.update_file_path(code_file)

        if problem_id and self.problem_title and self.contest_number:
            self.ui.create_problem_tab(
                problem_id,
                self.problem_title,
                self.contest_number,
                problem_info["test_cases"],
            )

        self.test_runner.update_test_cases(problem_info["test_cases"])

        status_message = self.code_manager.get_input_analysis_status()
        self.ui.update_input_analysis_status(status_message)

    def run_all_tests(self):
        """すべてのテストケースを実行"""
        current_tab = self.ui.notebook.index("current")

        # HTML入力タブかテストケースタブ
        if current_tab < 2:
            self.test_runner.run_all_tests()
            return

        tab_info = self.ui.get_current_tab_info()
        if tab_info and "problem_id" in tab_info:
            self.run_tests_for_problem(tab_info["problem_id"])

    def run_tests_for_problem(self, problem_id):
        """指定された問題のテストケースを実行"""
        if problem_id not in self.problems:
            self.ui.show_status_message(
                f"問題IDが見つかりません: {problem_id}", "Warning.TLabel"
            )
            return

        tab_info = self.ui.get_problem_tab_info(problem_id)
        if not tab_info:
            self.ui.show_status_message(
                f"テストケース情報が見つかりません", "Warning.TLabel"
            )
            return

        code_file = self.code_manager.code_file
        if not code_file or not os.path.exists(code_file):
            self.ui.show_status_message(
                "Pythonファイルが存在しません", "Warning.TLabel"
            )
            return

        self.test_runner.run_tests_for_tab(tab_info)

    def generate_single_file(self):
        """ファイルを生成"""
        self.code_manager.generate_file()

    def on_closing(self):
        """アプリケーション終了時の処理"""
        if hasattr(self, "file_monitor"):
            self.file_monitor.stop()

        if hasattr(self, "clipboard_monitor"):
            self.clipboard_monitor.stop()

        self.root.destroy()
