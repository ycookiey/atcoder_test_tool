import tkinter as tk
from tkinter import ttk
from ui.widgets import create_scrolledtext
from ui.styles import COLOR_BG_MEDIUM


class MainWindow:
    """メインウィンドウとUIコンポーネントを管理するクラス"""

    def __init__(self, root, app_controller):
        self.root = root
        self.app_controller = app_controller

        # メインフレームの作成
        self.main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # UIコンポーネントの初期化
        self._create_header()
        self._create_loading_indicator()
        self._create_notebook()

        # 初期タブをHTML入力タブに設定
        self.notebook.select(0)
        self.enable_testcase_tab(False)
        # MainWindowクラスの__init__メソッド内に以下を追加
        menubar = tk.Menu(root)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(
            label="コピー(コメント除去) Ctrl+C",
            command=lambda: self.app_controller.code_manager.copy_without_comments(),
            accelerator="Ctrl+C",
        )
        menubar.add_cascade(label="編集", menu=editmenu)
        root.config(menu=menubar)

        # rootレベルでバインド
        root.bind(
            "<Control-c>",
            lambda e: self.app_controller.code_manager.copy_without_comments(),
        )

    def _create_header(self):
        """ヘッダーエリアを作成"""
        # ヘッダーフレーム（問題情報とステータス）
        header_frame = ttk.Frame(self.main_frame, style="Medium.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 5))

        # 問題情報ラベル
        self.info_label = ttk.Label(
            header_frame, text="AtCoder Test Tool", style="Header.TLabel"
        )
        self.info_label.pack(side=tk.LEFT, padx=10, pady=5)

        # ステータスメッセージ
        self.status_label = ttk.Label(header_frame, text="", style="Status.TLabel")
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def _create_loading_indicator(self):
        """ローディングインジケータを作成"""
        # 解析中インジケータフレーム
        self.loading_frame = ttk.Frame(self.main_frame, style="Medium.TFrame")
        self.loading_frame.pack(fill=tk.X, pady=(0, 5))

        # プログレスバー
        self.progress_bar = ttk.Progressbar(
            self.loading_frame, mode="indeterminate", style="TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, padx=10)

        # 解析中メッセージ
        self.loading_label = ttk.Label(
            self.loading_frame, text="HTMLを解析中...", style="Loading.TLabel"
        )
        self.loading_label.pack(pady=(0, 5))

        # 初期状態では非表示
        self.loading_frame.pack_forget()

    def _create_notebook(self):
        """タブ付きインターフェース（ノートブック）を作成"""
        # メインコンテンツ用のノートブック
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # タブ変更イベントをバインド
        self.notebook.bind("<<NotebookTabChanged>>", self.app_controller.on_tab_changed)

        # === HTML入力タブ ===
        self._create_html_tab()

        # === テストケースタブ ===
        self._create_test_tab()

    def _create_html_tab(self):
        """HTML入力タブを作成"""
        html_tab = ttk.Frame(self.notebook, style="Medium.TFrame")
        self.notebook.add(html_tab, text="HTML入力")

        # HTML入力エリアのヘッダー
        html_header = ttk.Frame(html_tab, style="Medium.TFrame")
        html_header.pack(fill=tk.X, padx=10, pady=(10, 5))

        html_label = ttk.Label(
            html_header, text="AtCoderのHTMLを貼り付け:", style="TLabel"
        )
        html_label.pack(side=tk.LEFT)

        # クリップボードから貼り付けボタン
        paste_button = ttk.Button(
            html_header,
            text="クリップボードから貼り付け",
            command=self.app_controller.paste_from_clipboard,
            style="Primary.TButton",
        )
        paste_button.pack(side=tk.RIGHT)

        # HTML入力エリア
        self.html_text = create_scrolledtext(html_tab, height=6)
        self.html_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # HTMLテキストエリアの変更を監視
        self.html_text.bind("<KeyRelease>", self.app_controller.on_html_change)

    def _create_test_tab(self):
        """テストケースタブを作成"""
        test_tab = ttk.Frame(self.notebook, style="Medium.TFrame")
        self.notebook.add(test_tab, text="テストケース")

        # テスト画面の分割（水平方向）
        test_split = ttk.PanedWindow(test_tab, orient=tk.HORIZONTAL)
        test_split.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左側のコードエリア
        left_frame = ttk.Frame(test_split, style="Medium.TFrame")
        test_split.add(left_frame, weight=1)

        # コードフレーム
        self.code_frame = ttk.LabelFrame(left_frame, text="コード未選択")
        self.code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # コードテキスト
        self.code_text = create_scrolledtext(
            self.code_frame, height=5, width=30, readonly=True
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 全テスト実行ボタン
        button_frame = ttk.Frame(left_frame, style="Medium.TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        vscode_btn = ttk.Button(
            button_frame,
            text="VSCodeで開く",
            command=lambda: self.app_controller.code_manager.open_in_vscode(),
            style="Primary.TButton",
        )
        vscode_btn.pack(side=tk.LEFT, padx=5)

        # コメント除去してコピーするボタンを追加
        copy_clean_btn = ttk.Button(
            button_frame,
            text="コピー",
            command=lambda: self.app_controller.code_manager.copy_without_comments(),
            style="Primary.TButton",
        )
        copy_clean_btn.pack(side=tk.LEFT, padx=5)

        run_all_btn = ttk.Button(
            button_frame,
            text="全テストケース実行",
            command=self.app_controller.run_all_tests,
            style="Primary.TButton",
        )
        run_all_btn.pack(side=tk.LEFT, padx=5)

        # 右側のテストケースエリア
        right_frame = ttk.Frame(test_split, style="Medium.TFrame")
        test_split.add(right_frame, weight=3)

        # テストケースコンテナのスクロール機能
        self.test_canvas = tk.Canvas(
            right_frame, bg=COLOR_BG_MEDIUM, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            right_frame, orient="vertical", command=self.test_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.test_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.test_canvas.configure(yscrollcommand=scrollbar.set)

        # テストケースを格納するフレーム
        self.test_container = ttk.Frame(self.test_canvas, style="Medium.TFrame")
        window_id = self.test_canvas.create_window(
            (0, 0),
            window=self.test_container,
            anchor="nw",
            width=self.test_canvas.winfo_reqwidth(),
        )

        def on_canvas_configure(event):
            canvas_width = event.width
            self.test_canvas.itemconfig(window_id, width=canvas_width)
            self.test_canvas.configure(scrollregion=self.test_canvas.bbox("all"))

        self.test_container.bind(
            "<Configure>",
            lambda e: self.test_canvas.configure(
                scrollregion=self.test_canvas.bbox("all")
            ),
        )
        self.test_canvas.bind("<Configure>", on_canvas_configure)

    def show_loading(self, show=True):
        """解析中のローディング表示を切り替え"""
        if show:
            self.loading_frame.pack(
                fill=tk.X, pady=(0, 5), after=self.info_label.master
            )
            self.progress_bar.start(10)  # アニメーション速度を設定
        else:
            self.progress_bar.stop()
            self.loading_frame.pack_forget()

    def show_status_message(self, message, style="Status.TLabel", duration=3000):
        """ステータスメッセージを表示"""
        self.status_label.config(text=message, style=style)
        # 一定時間後にメッセージをクリア
        self.root.after(duration, lambda: self.status_label.config(text=""))

    def enable_testcase_tab(self, enable=True):
        """テストケースタブの有効/無効を切り替え"""
        if enable:
            self.notebook.tab(1, state="normal")
        else:
            self.notebook.tab(1, state="disabled")
