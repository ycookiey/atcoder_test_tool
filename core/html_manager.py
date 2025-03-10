import threading
from core.parser import parse_problem_html


class HTMLManager:
    """HTML解析を管理するクラス"""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.parsing = False

    def start_parsing(self, html_content):
        """HTML解析を別スレッドで開始"""
        if self.parsing:
            return False  # 既に解析中なら何もしない

        self.parsing = True
        self.app_controller.ui.show_loading(True)  # ローディング表示を開始

        # 別スレッドで解析を実行
        threading.Thread(
            target=self._parse_html_thread, args=(html_content,), daemon=True
        ).start()
        return True

    def _parse_html_thread(self, html_content):
        """別スレッドでHTML解析を実行"""
        try:
            problem_info = parse_problem_html(html_content)

            # 解析成功時は、メインスレッドで情報を更新して画面切り替え
            self.app_controller.root.after(
                0, lambda: self._on_parsing_complete(True, problem_info)
            )
        except Exception as e:
            print(f"HTMLの解析に失敗しました: {str(e)}")
            # 解析失敗時はエラーメッセージを表示
            self.app_controller.root.after(
                0, lambda: self._on_parsing_complete(False, None, str(e))
            )
        finally:
            # 解析終了フラグを設定
            self.parsing = False

    def _on_parsing_complete(self, success, problem_info=None, error_message=None):
        """解析完了時の処理"""
        self.app_controller.ui.show_loading(False)  # ローディング表示を終了

        if success and problem_info:
            # 問題情報を更新
            self.app_controller.update_problem_info(problem_info)

            if problem_info["test_cases"]:
                self.app_controller.ui.show_status_message(
                    f"{len(problem_info['test_cases'])}個のテストケースを解析しました",
                    "Success.TLabel",
                )

                # 問題タブに切り替え（もし作成されていれば）
                if problem_info["problem_id"] in self.app_controller.ui.problem_tabs:
                    tab_id = self.app_controller.ui.problem_tabs[
                        problem_info["problem_id"]
                    ]
                    self.app_controller.ui.notebook.select(tab_id)
                # そうでなければテストケースタブに切り替え（従来の挙動）
                else:
                    self.app_controller.ui.notebook.select(1)
        else:
            self.app_controller.ui.show_status_message(
                f"HTMLの解析に失敗しました: {error_message}", "Error.TLabel"
            )
