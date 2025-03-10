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

        # 問題タブ管理の初期化
        self.problem_tabs = {}  # 問題ID -> タブIDのマッピング
        self.tab_test_frames = {}  # タブID -> テストフレームのマッピング

        # メニューバーの設定
        menubar = tk.Menu(root)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(
            label="コピー(コメント除去) Ctrl+C",
            command=lambda: self.app_controller.code_manager.copy_without_comments(),
            accelerator="Ctrl+C",
        )
        menubar.add_cascade(label="編集", menu=editmenu)

        # 表示メニューを追加
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(
            label="次のタブ",
            command=self._next_tab,
            accelerator="Ctrl+Tab",
        )
        viewmenu.add_command(
            label="前のタブ",
            command=self._prev_tab,
            accelerator="Ctrl+Shift+Tab",
        )
        menubar.add_cascade(label="表示", menu=viewmenu)

        # 実行メニューを追加
        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(
            label="テスト実行",
            command=self.app_controller.run_all_tests,
            accelerator="F5",
        )
        menubar.add_cascade(label="実行", menu=runmenu)

        root.config(menu=menubar)

        # キーボードショートカットの設定
        root.bind(
            "<Control-c>",
            lambda e: self.app_controller.code_manager.copy_without_comments(),
        )

        # テスト実行のショートカットキー（F5）を設定
        root.bind("<F5>", lambda e: self.app_controller.run_all_tests())

        # タブ切り替えショートカットの設定
        self._setup_keyboard_shortcuts()

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
            text="全テストケース実行 (F5)",
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

    def create_problem_tab(self, problem_id, problem_title, contest_number, test_cases):
        """問題ごとのタブを作成"""
        # 既に同じ問題のタブが存在する場合は選択して終了
        if problem_id in self.problem_tabs:
            tab_id = self.problem_tabs[problem_id]
            self.notebook.select(tab_id)
            return

        # タブタイトル
        tab_title = f"{problem_id}: {problem_title}"

        # 新しいタブを作成
        problem_tab = ttk.Frame(self.notebook, style="Medium.TFrame")
        self.notebook.add(problem_tab, text=tab_title)

        # タブインデックスを保存
        tab_index = self.notebook.index(problem_tab)
        self.problem_tabs[problem_id] = tab_index

        # テスト画面の分割（水平方向）
        test_split = ttk.PanedWindow(problem_tab, orient=tk.HORIZONTAL)
        test_split.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左側のコードエリア
        left_frame = ttk.Frame(test_split, style="Medium.TFrame")
        test_split.add(left_frame, weight=1)

        # コードファイル名の設定
        code_file = self.app_controller.code_manager.update_code_file_path(
            contest_number, problem_id
        )

        # コードフレーム
        code_frame = ttk.LabelFrame(
            left_frame, text=code_file if code_file else "コード未選択"
        )
        code_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # コードテキスト
        code_text = create_scrolledtext(code_frame, height=5, width=30, readonly=True)
        code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ボタンフレーム
        button_frame = ttk.Frame(left_frame, style="Medium.TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # VSCodeで開くボタン
        vscode_btn = ttk.Button(
            button_frame,
            text="VSCodeで開く",
            command=lambda: self.app_controller.code_manager.open_in_vscode(),
            style="Primary.TButton",
        )
        vscode_btn.pack(side=tk.LEFT, padx=5)

        # コピーボタン
        copy_btn = ttk.Button(
            button_frame,
            text="コピー",
            command=lambda: self.app_controller.code_manager.copy_without_comments(),
            style="Primary.TButton",
        )
        copy_btn.pack(side=tk.LEFT, padx=5)

        # このタブのテストケースのみ実行するボタン
        run_btn = ttk.Button(
            button_frame,
            text="テスト実行 (F5)",
            command=lambda pid=problem_id: self.app_controller.run_tests_for_problem(
                pid
            ),
            style="Primary.TButton",
        )
        run_btn.pack(side=tk.LEFT, padx=5)

        # 右側のテストケースエリア
        right_frame = ttk.Frame(test_split, style="Medium.TFrame")
        test_split.add(right_frame, weight=3)

        # テストケースコンテナのスクロール機能
        test_canvas = tk.Canvas(right_frame, bg=COLOR_BG_MEDIUM, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            right_frame, orient="vertical", command=test_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        test_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        test_canvas.configure(yscrollcommand=scrollbar.set)

        # テストケースを格納するフレーム
        test_container = ttk.Frame(test_canvas, style="Medium.TFrame")
        window_id = test_canvas.create_window(
            (0, 0),
            window=test_container,
            anchor="nw",
            width=test_canvas.winfo_reqwidth(),
        )

        def on_canvas_configure(event):
            canvas_width = event.width
            test_canvas.itemconfig(window_id, width=canvas_width)
            test_canvas.configure(scrollregion=test_canvas.bbox("all"))

        test_container.bind(
            "<Configure>",
            lambda e: test_canvas.configure(scrollregion=test_canvas.bbox("all")),
        )
        test_canvas.bind("<Configure>", on_canvas_configure)

        # タブ情報を保存
        self.tab_test_frames[tab_index] = {
            "code_frame": code_frame,
            "code_text": code_text,
            "test_container": test_container,
            "problem_id": problem_id,
            "test_cases": [],
        }

        # テストケースを表示
        self.update_problem_tab_test_cases(problem_id, test_cases)

        # 新しいタブを選択
        self.notebook.select(tab_index)

        return tab_index

    def update_problem_tab_test_cases(self, problem_id, test_cases):
        """問題タブのテストケースを更新"""
        if problem_id not in self.problem_tabs:
            return False

        tab_index = self.problem_tabs[problem_id]
        if tab_index not in self.tab_test_frames:
            return False

        tab_info = self.tab_test_frames[tab_index]
        test_container = tab_info["test_container"]

        # テストケースコンテナをクリア
        for widget in test_container.winfo_children():
            widget.destroy()

        # テストケースを表示
        from ui.test_case_frame import TestCaseFrame

        tab_test_cases = []
        for i, test_case in enumerate(test_cases):
            # フレームを作成
            test_frame = TestCaseFrame(
                test_container,
                f"テストケース {i+1}",
            )
            test_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

            # コンテンツ部分（3列レイアウト）
            content_frame = test_frame.content_frame

            # 入力例（左）
            input_frame = ttk.Frame(content_frame, style="Light.TFrame")
            input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(input_frame, text=test_case["input_title"], style="TLabel").pack(
                anchor=tk.W, padx=5, pady=2
            )
            input_text = create_scrolledtext(input_frame, height=6, width=30)
            input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            input_text.insert(tk.END, test_case["input"])

            # 期待される出力（中央）
            expected_frame = ttk.Frame(content_frame, style="Light.TFrame")
            expected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(
                expected_frame, text=test_case["output_title"], style="TLabel"
            ).pack(anchor=tk.W, padx=5, pady=2)
            expected_text = create_scrolledtext(expected_frame, height=6, width=30)
            expected_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            expected_text.insert(tk.END, test_case["expected_output"])

            # 実際の出力（右）
            actual_frame = ttk.Frame(content_frame, style="Light.TFrame")
            actual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(actual_frame, text="実際の出力", style="TLabel").pack(
                anchor=tk.W, padx=5, pady=2
            )
            actual_text = create_scrolledtext(actual_frame, height=6, width=30)
            actual_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # テストケース情報を保存
            case_info = {
                "input_title": test_case["input_title"],
                "input": test_case["input"],
                "output_title": test_case["output_title"],
                "expected_output": test_case["expected_output"],
                "input_widget": input_text,
                "output_widget": expected_text,
                "actual_output_widget": actual_text,
                "result_frame": test_frame,
            }
            tab_test_cases.append(case_info)

        # タブのテストケース情報を更新
        self.tab_test_frames[tab_index]["test_cases"] = tab_test_cases

        return True

    def get_current_tab_info(self):
        """現在選択されているタブの情報を取得"""
        current_tab = self.notebook.index("current")

        # HTML入力タブかテストケースタブの場合
        if current_tab < 2:
            return None

        # 問題タブの場合
        if current_tab in self.tab_test_frames:
            return self.tab_test_frames[current_tab]

        return None

    def get_problem_tab_info(self, problem_id):
        """指定された問題IDのタブ情報を取得"""
        if problem_id not in self.problem_tabs:
            return None

        tab_index = self.problem_tabs[problem_id]
        if tab_index not in self.tab_test_frames:
            return None

        return self.tab_test_frames[tab_index]

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

    def _setup_keyboard_shortcuts(self):
        """キーボードショートカットを設定"""
        # Ctrl+Tab で次のタブへ
        self.root.bind("<Control-Tab>", self._next_tab)

        # Ctrl+Shift+Tab で前のタブへ
        self.root.bind("<Control-Shift-Tab>", self._prev_tab)

    def _next_tab(self, event=None):
        """次のタブに切り替え"""
        current = self.notebook.index("current")
        tabs = self.notebook.tabs()

        # 有効なタブのみを対象にする
        enabled_tabs = [
            tab for tab in tabs if self.notebook.tab(tab, "state") != "disabled"
        ]
        if not enabled_tabs:
            return

        # 現在のタブの位置を探す
        try:
            current_idx = enabled_tabs.index(tabs[current])
            next_idx = (current_idx + 1) % len(enabled_tabs)
            self.notebook.select(enabled_tabs[next_idx])
        except (ValueError, IndexError):
            # エラーが発生した場合は最初のタブを選択
            if enabled_tabs:
                self.notebook.select(enabled_tabs[0])

        return "break"  # イベントの伝播を停止

    def _prev_tab(self, event=None):
        """前のタブに切り替え"""
        current = self.notebook.index("current")
        tabs = self.notebook.tabs()

        # 有効なタブのみを対象にする
        enabled_tabs = [
            tab for tab in tabs if self.notebook.tab(tab, "state") != "disabled"
        ]
        if not enabled_tabs:
            return

        # 現在のタブの位置を探す
        try:
            current_idx = enabled_tabs.index(tabs[current])
            prev_idx = (current_idx - 1) % len(enabled_tabs)
            self.notebook.select(enabled_tabs[prev_idx])
        except (ValueError, IndexError):
            # エラーが発生した場合は最後のタブを選択
            if enabled_tabs:
                self.notebook.select(enabled_tabs[-1])

        return "break"  # イベントの伝播を停止
