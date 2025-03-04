from tkinter import ttk
from ui.styles import *


class ThemeManager:
    """アプリケーションのテーマを管理するクラス"""

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.setup_theme()

    def setup_theme(self):
        """ダークテーマのスタイルを設定"""
        # ウィンドウの背景色を設定
        self.root.configure(bg=COLOR_BG_DARK)

        # TFrame設定
        self.style.configure("TFrame", background=COLOR_BG_DARK)
        self.style.configure("Dark.TFrame", background=COLOR_BG_DARK)
        self.style.configure("Medium.TFrame", background=COLOR_BG_MEDIUM)
        self.style.configure("Light.TFrame", background=COLOR_BG_LIGHT)
        self.style.configure(
            "Highlight.TFrame", background=COLOR_PRIMARY, borderwidth=2
        )

        # TLabelframe設定
        self.style.configure(
            "TLabelframe", background=COLOR_BG_MEDIUM, foreground=COLOR_FG
        )
        self.style.configure(
            "TLabelframe.Label",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_ACCENT,
            font=("Arial", 10, "bold"),
        )

        # TLabel設定
        self.style.configure("TLabel", background=COLOR_BG_MEDIUM, foreground=COLOR_FG)
        self.style.configure(
            "Status.TLabel",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_ACCENT,
            font=("Arial", 10),
        )
        self.style.configure(
            "Header.TLabel",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_ACCENT,
            font=("Arial", 12, "bold"),
        )
        self.style.configure(
            "Success.TLabel", background=COLOR_BG_MEDIUM, foreground=COLOR_SUCCESS
        )
        self.style.configure(
            "Error.TLabel", background=COLOR_BG_MEDIUM, foreground=COLOR_ERROR
        )
        self.style.configure(
            "Warning.TLabel", background=COLOR_BG_MEDIUM, foreground=COLOR_WARNING
        )
        self.style.configure(
            "Loading.TLabel",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_WARNING,
            font=("Arial", 10, "bold"),
        )
        self.style.configure(
            "Running.TLabel", background=COLOR_BG_MEDIUM, foreground=COLOR_WARNING
        )

        # TButton設定
        self.style.configure(
            "TButton",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_FG,
            borderwidth=0,
            font=("Arial", 9),
            padding=5,
        )
        self.style.map(
            "TButton",
            background=[("active", COLOR_BG_LIGHT), ("pressed", COLOR_BG_DARK)],
            foreground=[("active", COLOR_ACCENT), ("pressed", COLOR_PRIMARY)],
        )

        # Primary.TButton設定（強調ボタン）
        self.style.configure(
            "Primary.TButton",
            background=COLOR_PRIMARY,
            foreground=COLOR_BG_DARK,
            borderwidth=0,
            font=("Arial", 9, "bold"),
            padding=5,
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", COLOR_ACCENT), ("pressed", COLOR_BG_LIGHT)],
            foreground=[("active", COLOR_BG_DARK), ("pressed", COLOR_ACCENT)],
        )

        # Icon.TButton設定（アイコンボタン）
        self.style.configure("Icon.TButton", padding=3, font=("Arial", 12))

        # TPanedwindow設定
        self.style.configure("TPanedwindow", background=COLOR_BG_DARK)

        # TNotebook設定
        self.style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_FG,
            padding=[5, 2],
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", COLOR_PRIMARY), ("disabled", COLOR_DISABLED)],
            foreground=[("selected", COLOR_BG_DARK), ("disabled", COLOR_BG_DARK)],
        )

        # スクロールバー設定
        self.style.configure(
            "Vertical.TScrollbar",
            background=COLOR_BG_LIGHT,
            troughcolor=COLOR_BG_MEDIUM,
            borderwidth=0,
        )
        self.style.map(
            "Vertical.TScrollbar",
            background=[("active", COLOR_PRIMARY), ("disabled", COLOR_DISABLED)],
        )

        # TProgressbar設定
        self.style.configure(
            "TProgressbar",
            troughcolor=COLOR_BG_MEDIUM,
            background=COLOR_PRIMARY,
            borderwidth=0,
            thickness=5,
        )
