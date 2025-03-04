import os
import time
import threading


class FileMonitor:
    def __init__(self, file_path, callback, interval=1.0):
        """
        ファイルの変更を監視するクラス

        Args:
            file_path: 監視するファイルのパス
            callback: ファイルが変更されたときに呼び出す関数
            interval: チェック間隔（秒）
        """
        self.file_path = file_path
        self.callback = callback
        self.interval = interval
        self.last_modified_time = 0
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
            if self.file_path and os.path.exists(self.file_path):
                current_mtime = os.path.getmtime(self.file_path)
                if current_mtime != self.last_modified_time:
                    self.last_modified_time = current_mtime
                    if self.callback:
                        self.callback()
            time.sleep(self.interval)

    def update_file_path(self, new_path):
        """監視するファイルを変更"""
        self.file_path = new_path
        self.last_modified_time = 0  # リセット
