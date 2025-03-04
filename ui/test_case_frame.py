import tkinter as tk
from tkinter import ttk
from ui.styles import COLOR_BG_MEDIUM, ICON_PENDING, ICON_SUCCESS, ICON_ERROR


class TestCaseFrame(ttk.Frame):
    """テストケースを表示するフレーム"""

    def __init__(self, parent, title, style="Medium.TFrame", **kwargs):
        ttk.Frame.__init__(self, parent, style=style)

        # ヘッダーフレーム
        self.header_frame = ttk.Frame(self, style="Dark.TFrame")
        self.header_frame.pack(fill=tk.X, padx=2, pady=2)

        # タイトル
        self.title_label = ttk.Label(
            self.header_frame, text=title, style="Header.TLabel"
        )
        self.title_label.pack(side=tk.LEFT, padx=5, pady=5)

        # 結果アイコン
        self.result_icon = ttk.Label(
            self.header_frame, text=ICON_PENDING, style="Status.TLabel"
        )
        self.result_icon.pack(side=tk.LEFT, padx=5, pady=5)

        # 結果ラベル
        self.result_label = ttk.Label(
            self.header_frame, text="未実行", style="Status.TLabel"
        )
        self.result_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # コンテンツフレーム
        self.content_frame = ttk.Frame(self, style="Light.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def set_result(self, passed=None):
        """テスト結果を設定"""
        if passed is None:
            self.result_icon.config(text=ICON_PENDING, style="Status.TLabel")
            self.result_label.config(text="未実行", style="Status.TLabel")
        elif passed:
            self.result_icon.config(text=ICON_SUCCESS, style="Success.TLabel")
            self.result_label.config(text="合格", style="Success.TLabel")
        else:
            self.result_icon.config(text=ICON_ERROR, style="Error.TLabel")
            self.result_label.config(text="不合格", style="Error.TLabel")
