import threading
import time
import re


class ClipboardMonitor:
    """クリップボードの変更を監視するクラス"""

    def __init__(self, app_controller, interval=0.5):
        """
        Args:
            app_controller: メインアプリケーションコントローラー
            interval: チェック間隔（秒）
        """
        self.app_controller = app_controller
        self.interval = interval
        self.last_clipboard_content = ""
        self.running = False
        self.thread = None

    def start(self):
        """監視を開始"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """監視を停止"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=self.interval * 2)
            self.thread = None

    def _monitor_loop(self):
        """監視ループ"""
        while self.running:
            try:
                # 現在のクリップボード内容を取得
                current_content = self.app_controller.root.clipboard_get()

                # 内容が変わっていて、かつHTML入力タブがアクティブな場合のみ処理
                if (
                    current_content != self.last_clipboard_content
                    and self._looks_like_atcoder_html(current_content)
                ):

                    # UIスレッドで安全に貼り付け
                    self.app_controller.root.after(
                        0, lambda: self._auto_paste(current_content)
                    )

                self.last_clipboard_content = current_content
            except Exception:
                # クリップボードが空または取得できない場合はスキップ
                pass

            time.sleep(self.interval)

    def _looks_like_atcoder_html(self, content):
        """コンテンツがAtCoderのHTML形式かどうかをチェック"""
        if len(content) < 100:  # 短すぎる内容は除外
            return False

        # AtCoderのHTMLに特徴的なパターンをチェック
        atcoder_patterns = [
            r'<span class="h2">[A-Z] - ',  # 問題タイトルパターン
            r'<div class="part">',  # 入力例、出力例のセクション
            r"<h3>入力例",  # 入力例のヘッダー
            r"<h3>出力例",  # 出力例のヘッダー
            r'<a href="/contests/abc\d+',  # コンテストへのリンク
        ]

        # いずれかのパターンにマッチすればAtCoderのHTMLとみなす
        for pattern in atcoder_patterns:
            if re.search(pattern, content):
                return True

        return False

    def _auto_paste(self, content):
        """コンテンツを自動的に貼り付け"""
        try:
            ui = self.app_controller.ui
            # 現在のHTML入力欄の内容をチェック
            current_text = ui.html_text.get("1.0", "end-1c").strip()

            # 入力欄が空、または別の内容の場合のみ貼り付け
            if not current_text or current_text != content.strip():
                ui.html_text.delete("1.0", "end")
                ui.html_text.insert("1.0", content)
                ui.show_status_message(
                    "クリップボードから自動貼り付けしました", "Success.TLabel"
                )

                # 明示的に解析を開始
                self.app_controller.start_parsing()
        except Exception as e:
            print(f"自動貼り付けに失敗しました: {e}")
