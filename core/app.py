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

        # 問題情報
        self.contest_number = ""
        self.problem_id = ""
        self.problem_title = ""

        # テーマの設定
        self.theme_manager = ThemeManager(root)

        # 各マネージャーの初期化
        self.html_manager = HTMLManager(self)
        self.test_runner = TestRunner(self)
        self.code_manager = CodeManager(self)

        # UIの初期化
        self.ui = MainWindow(root, self)

        # ファイル監視を開始
        self.file_monitor = FileMonitor("", self.code_manager.reload_code_file)
        self.file_monitor.start()

        # クリップボード監視を開始（追加）
        self.clipboard_monitor = ClipboardMonitor(self)
        self.clipboard_monitor.start()

    # イベントハンドラ
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
                # 明示的に解析を開始
                self.start_parsing()
        except Exception as e:
            self.ui.show_status_message(
                f"クリップボードからの貼り付けに失敗しました", "Error.TLabel"
            )

    def on_html_change(self, event=None):
        """HTMLテキストエリアの内容が変更されたらパースを実行"""
        html_content = self.ui.html_text.get("1.0", tk.END).strip()
        if len(html_content) > 100 and not self.html_manager.parsing:
            # 短すぎる内容は無視、かつ解析中でない場合
            self.start_parsing()

    def on_tab_changed(self, event):
        """タブ変更時のイベントハンドラ"""
        current_tab = self.ui.notebook.index(self.ui.notebook.select())
        if current_tab == 1:  # テストケースタブ
            html_content = self.ui.html_text.get("1.0", tk.END).strip()
            if not html_content or len(html_content) < 100:  # 内容が不十分
                self.ui.notebook.select(0)  # HTML入力タブに戻る
                self.ui.show_status_message("HTMLを入力してください", "Warning.TLabel")

    # 操作メソッド
    def start_parsing(self):
        """HTML解析を開始"""
        html_content = self.ui.html_text.get("1.0", tk.END)
        self.html_manager.start_parsing(html_content)

    def update_problem_info(self, problem_info):
        """問題情報を更新"""
        # 問題情報の保存
        self.problem_id = problem_info["problem_id"]
        self.problem_title = problem_info["problem_title"]
        self.contest_number = problem_info["contest_number"]

        # 問題情報の表示を更新
        if self.contest_number and self.problem_id and self.problem_title:
            info_text = (
                f"ABC {self.contest_number} - {self.problem_id}: {self.problem_title}"
            )
            self.ui.info_label.config(text=info_text)

            # コードファイル設定
            code_file = self.code_manager.update_code_file_path(
                self.contest_number, self.problem_id
            )

            # コード表示用フレームのタイトルを更新
            if code_file:
                self.code_manager.update_code_frame(code_file)

                # ファイル監視の更新
                self.file_monitor.update_file_path(code_file)

        # テストケースの更新
        self.test_runner.update_test_cases(problem_info["test_cases"])

    def run_all_tests(self):
        """すべてのテストケースを実行"""
        self.test_runner.run_all_tests()

    def generate_single_file(self):
        """ファイルを生成"""
        self.code_manager.generate_file()

    def on_closing(self):
        """アプリケーション終了時の処理"""
        # 各監視スレッドを停止
        if hasattr(self, "file_monitor"):
            self.file_monitor.stop()

        if hasattr(self, "clipboard_monitor"):
            self.clipboard_monitor.stop()

        # ウィンドウを閉じる
        self.root.destroy()
