import os
import threading
import time
from ui.test_case_frame import TestCaseFrame
from ui.widgets import create_scrolledtext
import tkinter as tk
from tkinter import ttk
from core.tester import run_python_test, compare_outputs
from ui.styles import ICON_WARNING
import concurrent.futures


class TestRunner:
    """テストケースの実行と結果表示を管理するクラス"""

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.test_cases = []

    def clear_test_cases(self):
        """テストケースをクリア"""
        self.test_cases = []

    def update_test_cases(self, test_cases):
        """テストケースを更新"""
        self.test_cases = test_cases
        self._update_test_ui()

    def _update_test_ui(self):
        """テストケースのUIを更新"""
        ui = self.app_controller.ui

        # テストケースコンテナをクリア
        for widget in ui.test_container.winfo_children():
            widget.destroy()

        # テストケースを表示
        for i, test_case in enumerate(self.test_cases):
            # 通常のフレームを作成（常に展開）
            test_frame = TestCaseFrame(
                ui.test_container,
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
            test_case["input_widget"] = input_text

            # 期待される出力（中央）
            expected_frame = ttk.Frame(content_frame, style="Light.TFrame")
            expected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(
                expected_frame, text=test_case["output_title"], style="TLabel"
            ).pack(anchor=tk.W, padx=5, pady=2)
            expected_text = create_scrolledtext(expected_frame, height=6, width=30)
            expected_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            expected_text.insert(tk.END, test_case["expected_output"])
            test_case["output_widget"] = expected_text

            # 実際の出力（右）
            actual_frame = ttk.Frame(content_frame, style="Light.TFrame")
            actual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(actual_frame, text="実際の出力", style="TLabel").pack(
                anchor=tk.W, padx=5, pady=2
            )
            actual_text = create_scrolledtext(actual_frame, height=6, width=30)
            actual_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            test_case["actual_output_widget"] = actual_text

            # 結果表示用の参照を保持
            test_case["result_frame"] = test_frame

        # テストケースがあればタブを有効化
        if self.test_cases:
            self.app_controller.ui.enable_testcase_tab(True)

    def run_all_tests(self):
        """すべてのテストケースを実行"""
        if not self.test_cases:
            self.app_controller.ui.show_status_message(
                "テストケースがありません", "Warning.TLabel"
            )
            return

        code_file = self.app_controller.code_manager.code_file
        if not code_file or not os.path.exists(code_file):
            self.app_controller.ui.show_status_message(
                "Pythonファイルが存在しません", "Warning.TLabel"
            )
            return

        # 別スレッドで実行してUIをブロックしないようにする
        threading.Thread(target=self._run_all_tests_thread).start()

    def _run_all_tests_thread(self):
        """並列ですべてのテストを実行"""
        # まず全てのテストの出力をクリア
        for i in range(len(self.test_cases)):
            test_case = self.test_cases[i]

            # UIスレッドで安全に更新
            def clear_output(index):
                test_case = self.test_cases[index]
                actual_output_widget = test_case["actual_output_widget"]
                actual_output_widget.config(state="normal")
                actual_output_widget.delete("1.0", tk.END)
                # クリア後にdisabledにしない - これが出力が表示されない原因
                test_case["result_frame"].set_running()

            self.app_controller.root.after(0, lambda idx=i: clear_output(idx))

        # UIが更新される時間を少し待つ
        time.sleep(0.1)

        # 並列処理のためのスレッドプール
        all_passed = True
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(4, len(self.test_cases))
        ) as executor:
            # テスト実行をスレッドプールに投入
            future_to_test = {
                executor.submit(self._run_test, i): i
                for i in range(len(self.test_cases))
            }

            # 完了したテストの結果を処理
            for future in concurrent.futures.as_completed(future_to_test):
                test_index = future_to_test[future]
                try:
                    passed = future.result()
                    if not passed:
                        all_passed = False
                except Exception as e:
                    print(
                        f"テスト {test_index} の実行中にエラーが発生しました: {str(e)}"
                    )
                    all_passed = False

        # 結果を表示
        if all_passed:
            self.app_controller.ui.show_status_message(
                "すべてのテストに合格しました！", "Success.TLabel"
            )
        else:
            self.app_controller.ui.show_status_message(
                "テストに不合格があります", "Error.TLabel"
            )

    def _run_test(self, test_index):
        """指定されたインデックスのテストケースを実行"""
        code_file = self.app_controller.code_manager.code_file
        if not code_file or not os.path.exists(code_file):
            self.app_controller.ui.show_status_message(
                "Pythonファイルが存在しません", "Warning.TLabel"
            )
            return False

        test_case = self.test_cases[test_index]

        # 入力と期待される出力を取得（ウィジェットから最新の値を取得）
        input_data = test_case["input_widget"].get("1.0", tk.END).strip()
        expected_output = test_case["output_widget"].get("1.0", tk.END).strip()

        try:
            # テスト実行
            result = run_python_test(code_file, input_data)

            # 実際の出力を表示
            actual_output_widget = test_case["actual_output_widget"]
            result_frame = test_case["result_frame"]

            # UIスレッドで安全に更新
            def update_ui():
                # 出力結果を表示
                actual_output_widget.config(state="normal")  # 編集可能に
                actual_output_widget.delete("1.0", tk.END)
                actual_output_widget.insert(tk.END, result["output"])

                # 結果を比較
                passed = compare_outputs(result["output"], expected_output)

                # 結果ラベルを更新
                result_frame.set_result(passed)

                # エラーがあれば表示
                if result["error"]:
                    actual_output_widget.insert(
                        tk.END, f"\n\n--- エラー出力 ---\n{result['error']}"
                    )

                # 状態を読み取り専用に戻す必要がある場合はここでセット
                # actual_output_widget.config(state="disabled")

            # UIスレッドで更新
            self.app_controller.root.after(0, update_ui)

            # 大文字小文字を区別せずに比較
            passed = compare_outputs(result["output"], expected_output)

            # 処理が完了するまで少し待機して、UIの更新が反映されるようにする
            time.sleep(0.1)

            return passed

        except Exception as e:
            # エラーメッセージを表示
            def show_error():
                test_case["actual_output_widget"].config(state="normal")
                test_case["actual_output_widget"].delete("1.0", tk.END)
                test_case["actual_output_widget"].insert(
                    tk.END, f"エラーが発生しました: {str(e)}"
                )
                test_case["result_frame"].result_icon.config(
                    text=ICON_WARNING, style="Warning.TLabel"
                )
                test_case["result_frame"].result_label.config(
                    text="エラー", style="Error.TLabel"
                )
                # test_case["actual_output_widget"].config(state="disabled")

            self.app_controller.root.after(0, show_error)
            return False
