import os
import tkinter as tk
from tkinter import ttk


class CodeManager:
    """コードファイルの生成と管理を行うクラス"""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.code_file = ""

    def update_code_file_path(self, contest_number, problem_id):
        """コードファイルのパスを更新"""
        if contest_number and problem_id:
            self.code_file = f"../{contest_number}{problem_id}.py"
            return self.code_file
        return None

    def update_code_frame(self, title):
        """コード表示用フレームを更新"""
        ui = self.app_controller.ui

        # フレームのタイトルを更新
        ui.code_frame.configure(text=title)

        # 既存のコードウィジェットをクリア
        for widget in ui.code_frame.winfo_children():
            widget.destroy()

        # ファイル生成ボタンを表示（ファイルが存在しない場合のみ）
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

        # コードテキストエリア (かなり小さく)
        from ui.widgets import create_scrolledtext

        ui.code_text = create_scrolledtext(
            ui.code_frame, height=5, width=30, readonly=True
        )
        ui.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ファイルが存在すれば読み込む
        if os.path.exists(self.code_file):
            self.app_controller.file_monitor.update_file_path(self.code_file)
            self.reload_code_file()

    def reload_code_file(self):
        """コードファイルを再読み込みして表示を更新"""
        try:
            if self.code_file and os.path.exists(self.code_file):
                with open(self.code_file, "r", encoding="utf-8") as f:
                    code = f.read()

                # UIスレッドでの更新
                self.app_controller.root.after(0, lambda: self.update_code_text(code))
        except Exception as e:
            print(f"ファイルの再読み込みに失敗: {str(e)}")

    def update_code_text(self, code):
        """コードテキストエリアを更新"""
        ui = self.app_controller.ui
        if hasattr(ui, "code_text"):
            ui.code_text.config(state="normal")
            ui.code_text.delete("1.0", tk.END)
            ui.code_text.insert(tk.END, code)
            ui.code_text.config(state="disabled")

    def generate_code_template(self):
        """コードテンプレートを生成"""
        template = """import bisect,collections,copy,heapq,itertools,math,numpy,string
import sys
def I(): return int(sys.stdin.readline().rstrip())
def LI(): return list(map(int,sys.stdin.readline().rstrip().split()))
def S(): return sys.stdin.readline().rstrip()
def LS(): return list(sys.stdin.readline().rstrip().split())
N = I()
A = [LI() for _ in range(N)]

"""
        return template

    def generate_file(self):
        """コードファイルを生成"""
        if not self.code_file:
            return

        # テンプレートコードを取得
        template = self.generate_code_template()

        try:
            # ファイルに保存
            with open(self.code_file, "w", encoding="utf-8") as f:
                f.write(template)

            # コードフレームを更新（ファイル生成ボタンを削除）
            frame_title = f"{self.code_file}"
            self.update_code_frame(frame_title)

            # 成功メッセージをステータスバーに表示
            self.app_controller.ui.show_status_message(
                f"ファイルを生成しました: {self.code_file}", "Success.TLabel"
            )
        except Exception as e:
            self.app_controller.ui.show_status_message(
                f"ファイルの生成に失敗しました: {str(e)}", "Error.TLabel"
            )
