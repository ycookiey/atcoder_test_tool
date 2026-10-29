import os
import tkinter as tk
from tkinter import ttk
import subprocess
import re
from .input_analysis.input_analyzer import InputAnalyzer


class CodeManager:
    """コードファイルの生成と管理を行うクラス"""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.code_file = ""
        self.input_analyzer = InputAnalyzer()
        self.current_problem_info = None

    def update_code_file_path(self, contest_number, problem_id):
        """コードファイルのパスを更新"""
        if contest_number and problem_id:
            self.code_file = f"{contest_number}{problem_id}.py"
            return self.code_file
        return None

    def set_current_problem_info(self, problem_info):
        """現在の問題情報を設定"""
        self.current_problem_info = problem_info

    def update_code_frame(self, title):
        """コード表示用フレームを更新"""
        ui = self.app_controller.ui

        ui.code_frame.configure(text=title)

        for widget in ui.code_frame.winfo_children():
            widget.destroy()

        if self.code_file and not os.path.exists(self.code_file):
            file_gen_frame = ttk.Frame(ui.code_frame, style="Medium.TFrame")
            file_gen_frame.pack(fill=tk.X, pady=5, padx=5)

            message_label = ttk.Label(
                file_gen_frame,
                text=f"ファイル {self.code_file} が見つかりません",
                style="Warning.TLabel",
            )
            message_label.pack(side=tk.LEFT, padx=(0, 10))

            gen_button = ttk.Button(
                file_gen_frame,
                text="ファイルを生成",
                command=self.generate_file,
                style="Primary.TButton",
            )
            gen_button.pack(side=tk.RIGHT)

        from ui.widgets import create_scrolledtext

        ui.code_text = create_scrolledtext(
            ui.code_frame, height=5, width=30, readonly=True
        )
        ui.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        if os.path.exists(self.code_file):
            self.app_controller.file_monitor.update_file_path(self.code_file)
            self.reload_code_file()

        current_tab = self.app_controller.ui.notebook.index("current")
        if current_tab >= 2:  # HTML入力とテストケース以外のタブ
            tab_info = self.app_controller.ui.get_current_tab_info()
            if tab_info and "code_text" in tab_info:
                self.update_problem_tab_code(tab_info, title)

    def update_problem_tab_code(self, tab_info, title=None):
        """問題タブのコード表示を更新"""
        if not tab_info or "code_frame" not in tab_info or "code_text" not in tab_info:
            return

        code_frame = tab_info["code_frame"]
        code_text = tab_info["code_text"]

        try:
            code_frame.winfo_exists()
            code_text.winfo_exists()
        except tk.TclError:
            # ウィジェットが削除されている場合は何もしない
            return

        if title:
            code_frame.configure(text=title)

        if self.code_file and not os.path.exists(self.code_file):
            for widget in code_frame.winfo_children():
                if widget != code_text:
                    widget.destroy()

            file_gen_frame = ttk.Frame(code_frame, style="Medium.TFrame")
            file_gen_frame.pack(fill=tk.X, pady=5, padx=5)

            message_label = ttk.Label(
                file_gen_frame,
                text=f"ファイル {self.code_file} が見つかりません",
                style="Warning.TLabel",
            )
            message_label.pack(side=tk.LEFT, padx=(0, 10))

            gen_button = ttk.Button(
                file_gen_frame,
                text="ファイルを生成",
                command=self.generate_file,
                style="Primary.TButton",
            )
            gen_button.pack(side=tk.RIGHT)

        if os.path.exists(self.code_file):
            try:
                with open(self.code_file, "r", encoding="utf-8") as f:
                    code = f.read()

                code_text.config(state="normal")
                code_text.delete("1.0", tk.END)
                code_text.insert(tk.END, code)
                code_text.config(state="disabled")
            except tk.TclError:
                # ウィジェットが削除されている場合は何もしない
                pass
            except Exception as e:
                try:
                    code_text.config(state="normal")
                    code_text.delete("1.0", tk.END)
                    code_text.insert(tk.END, f"ファイルの読み込みに失敗: {str(e)}")
                    code_text.config(state="disabled")
                except tk.TclError:
                    # ウィジェットが削除されている場合は何もしない
                    pass

    def reload_code_file(self):
        """コードファイルを再読み込みして表示を更新"""
        try:
            if self.code_file and os.path.exists(self.code_file):
                with open(self.code_file, "r", encoding="utf-8") as f:
                    code = f.read()

                self.app_controller.root.after(0, lambda: self.update_code_text(code))

                current_tab = self.app_controller.ui.notebook.index("current")
                if current_tab >= 2:  # 問題タブの場合
                    tab_info = self.app_controller.ui.get_current_tab_info()
                    if tab_info:
                        self.app_controller.root.after(
                            0, lambda: self.update_problem_tab_code(tab_info)
                        )
        except Exception as e:
            print(f"ファイルの再読み込みに失敗: {str(e)}")

    def update_code_text(self, code):
        """コードテキストエリアを更新"""
        ui = self.app_controller.ui
        if hasattr(ui, "code_text"):
            try:
                ui.code_text.config(state="normal")
                ui.code_text.delete("1.0", tk.END)
                ui.code_text.insert(tk.END, code)
                ui.code_text.config(state="disabled")
            except tk.TclError:
                # ウィジェットが削除されている場合は何もしない
                pass

    def generate_code_template(self, problem_info=None):
        """コードテンプレートを生成（入力解析結果があれば適用）"""

        base_template = """import bisect,collections,copy,heapq,itertools,math,numpy,string
import sys
def I(): return int(sys.stdin.readline().rstrip())
def LI(): return list(map(int,sys.stdin.readline().rstrip().split()))
def S(): return sys.stdin.readline().rstrip()
def LS(): return list(sys.stdin.readline().rstrip().split())

"""

        if problem_info and "input_format" in problem_info and "samples" in problem_info:
            input_format = problem_info["input_format"]
            samples = problem_info["samples"]

            if input_format and samples:
                prediction_result = self.input_analyzer.analyze_input_format(input_format, samples)

                if prediction_result:
                    generated_code = self.input_analyzer.generate_python_code(prediction_result)
                    return base_template + generated_code

        fallback_input = """N = I()
A = [LI() for _ in range(N)]

# TODO: 問題解決のロジックを実装"""

        return base_template + fallback_input

    def generate_file(self, problem_info=None):
        """コードファイルを生成（問題情報があれば入力解析を実行）"""
        if not self.code_file:
            return

        if problem_info is None:
            problem_info = self.current_problem_info

        template = self.generate_code_template(problem_info)

        try:
            with open(self.code_file, "w", encoding="utf-8") as f:
                f.write(template)

            frame_title = f"{self.code_file}"
            self.update_code_frame(frame_title)

            self.app_controller.ui.show_status_message(
                f"ファイルを生成しました: {self.code_file}", "Success.TLabel"
            )

            self.open_in_vscode()

            current_tab = self.app_controller.ui.notebook.index("current")
            if current_tab >= 2:  # 問題タブの場合
                tab_info = self.app_controller.ui.get_current_tab_info()
                if tab_info:
                    self.update_problem_tab_code(tab_info, frame_title)

        except Exception as e:
            self.app_controller.ui.show_status_message(
                f"ファイルの生成に失敗しました: {str(e)}", "Error.TLabel"
            )

    def open_in_vscode(self):
        """コードファイルをVSCodeで開く"""
        if not self.code_file or not os.path.exists(self.code_file):
            self.app_controller.ui.show_status_message(
                "開くファイルがありません", "Warning.TLabel"
            )
            return

        try:
            subprocess.Popen(["code", self.code_file], shell=True)
            self.app_controller.ui.show_status_message(
                f"VSCodeでファイルを開きました: {self.code_file}", "Success.TLabel"
            )
        except Exception as e:
            self.app_controller.ui.show_status_message(
                f"VSCodeでの開始に失敗しました: {str(e)}", "Error.TLabel"
            )

    def strip_comments(self, code):
        """Pythonコードからコメントを削除する"""
        lines = []
        for line in code.split("\n"):
            if re.match(r"^\s*#", line):
                continue

            commented_line = re.sub(r"#.*$", "", line)
            lines.append(commented_line.rstrip())

        result = []
        prev_empty = False
        for line in lines:
            is_empty = not line.strip()
            if not (is_empty and prev_empty):
                result.append(line)
            prev_empty = is_empty

        return "\n".join(result).strip()

    def copy_without_comments(self):
        """コメントを除いたコードをクリップボードにコピー"""
        if not self.code_file or not os.path.exists(self.code_file):
            self.app_controller.ui.show_status_message(
                "コピーするコードがありません", "Warning.TLabel"
            )
            return

        try:
            with open(self.code_file, "r", encoding="utf-8") as f:
                code = f.read()

            clean_code = self.strip_comments(code)

            self.app_controller.root.clipboard_clear()
            self.app_controller.root.clipboard_append(clean_code)

            self.app_controller.ui.show_status_message(
                "コメントを除いたコードをクリップボードにコピーしました",
                "Success.TLabel",
            )
        except Exception as e:
            self.app_controller.ui.show_status_message(
                f"コードのコピーに失敗しました: {str(e)}", "Error.TLabel"
            )

    def get_input_analysis_status(self):
        """入力解析のステータスメッセージを取得"""
        return self.input_analyzer.get_analysis_status_message()
