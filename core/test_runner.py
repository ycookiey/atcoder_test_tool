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

        for widget in ui.test_container.winfo_children():
            widget.destroy()

        for i, test_case in enumerate(self.test_cases):
            test_frame = TestCaseFrame(
                ui.test_container,
                f"テストケース {i+1}",
            )
            test_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

            content_frame = test_frame.content_frame

            input_frame = ttk.Frame(content_frame, style="Light.TFrame")
            input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(input_frame, text=test_case["input_title"], style="TLabel").pack(
                anchor=tk.W, padx=5, pady=2
            )
            input_text = create_scrolledtext(input_frame, height=6, width=30)
            input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            input_text.insert(tk.END, test_case["input"])
            test_case["input_widget"] = input_text

            expected_frame = ttk.Frame(content_frame, style="Light.TFrame")
            expected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(
                expected_frame, text=test_case["output_title"], style="TLabel"
            ).pack(anchor=tk.W, padx=5, pady=2)
            expected_text = create_scrolledtext(expected_frame, height=6, width=30)
            expected_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            expected_text.insert(tk.END, test_case["expected_output"])
            test_case["output_widget"] = expected_text

            actual_frame = ttk.Frame(content_frame, style="Light.TFrame")
            actual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

            ttk.Label(actual_frame, text="実際の出力", style="TLabel").pack(
                anchor=tk.W, padx=5, pady=2
            )
            actual_text = create_scrolledtext(actual_frame, height=6, width=30)
            actual_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            test_case["actual_output_widget"] = actual_text

            test_case["result_frame"] = test_frame

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

        # UIを止めないよう、別のスレッドで実行する
        threading.Thread(target=self._run_all_tests_thread).start()

    def _run_all_tests_thread(self):
        """並列ですべてのテストを実行"""
        for i in range(len(self.test_cases)):
            test_case = self.test_cases[i]

            # ウィジェットはUIスレッドで操作する
            def clear_output(index):
                test_case = self.test_cases[index]
                actual_output_widget = test_case["actual_output_widget"]
                actual_output_widget.config(state="normal")
                actual_output_widget.delete("1.0", tk.END)
                # 実行結果を書き込むため、disabledに戻さない
                test_case["result_frame"].set_running()

            self.app_controller.root.after(0, lambda idx=i: clear_output(idx))

        # UIが更新される時間を少し待つ
        time.sleep(0.1)

        all_passed = True
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(4, len(self.test_cases))
        ) as executor:
            future_to_test = {
                executor.submit(self._run_test, i): i
                for i in range(len(self.test_cases))
            }

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

        if all_passed:
            self.app_controller.ui.show_status_message(
                "すべてのテストに合格しました！", "Success.TLabel"
            )
        else:
            self.app_controller.ui.show_status_message(
                "テストに不合格があります", "Error.TLabel"
            )

    def run_tests_for_tab(self, tab_info):
        """指定されたタブのテストケースを実行"""
        if not tab_info or "test_cases" not in tab_info or not tab_info["test_cases"]:
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

        # UIを止めないよう、別のスレッドで実行する
        threading.Thread(target=lambda: self._run_tab_tests_thread(tab_info)).start()

    def _run_tab_tests_thread(self, tab_info):
        """並列で指定されたタブのテストを実行"""
        test_cases = tab_info["test_cases"]

        for i in range(len(test_cases)):
            test_case = test_cases[i]

            # ウィジェットはUIスレッドで操作する
            def clear_output(test_case):
                actual_output_widget = test_case["actual_output_widget"]
                actual_output_widget.config(state="normal")
                actual_output_widget.delete("1.0", tk.END)
                # 実行結果を書き込むため、disabledに戻さない
                test_case["result_frame"].set_running()

            self.app_controller.root.after(0, lambda tc=test_case: clear_output(tc))

        # UIが更新される時間を少し待つ
        time.sleep(0.1)

        all_passed = True
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(4, len(test_cases))
        ) as executor:
            future_to_test = {
                executor.submit(self._run_tab_test, test_case): i
                for i, test_case in enumerate(test_cases)
            }

            for future in concurrent.futures.as_completed(future_to_test):
                test_index = future_to_test[future]
                try:
                    passed = future.result()
                    if not passed:
                        all_passed = False
                except Exception as e:
                    print(
                        f"タブテスト {test_index} の実行中にエラーが発生しました: {str(e)}"
                    )
                    all_passed = False

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

        input_data = test_case["input_widget"].get("1.0", tk.END).strip()
        expected_output = test_case["output_widget"].get("1.0", tk.END).strip()

        try:
            result = run_python_test(code_file, input_data)

            actual_output_widget = test_case["actual_output_widget"]
            result_frame = test_case["result_frame"]

            # ウィジェットはUIスレッドで操作する
            def update_ui():
                actual_output_widget.config(state="normal")
                actual_output_widget.delete("1.0", tk.END)
                actual_output_widget.insert(tk.END, result["output"])

                passed = compare_outputs(result["output"], expected_output)

                result_frame.set_result(passed)

                if result["error"]:
                    actual_output_widget.insert(
                        tk.END, f"\n\n--- エラー出力 ---\n{result['error']}"
                    )


            self.app_controller.root.after(0, update_ui)

            passed = compare_outputs(result["output"], expected_output)

            # 処理が完了するまで少し待機して、UIの更新が反映されるようにする
            time.sleep(0.1)

            return passed

        except Exception as e:
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

            self.app_controller.root.after(0, show_error)
            return False

    def _run_tab_test(self, test_case):
        """タブのテストケースを実行"""
        code_file = self.app_controller.code_manager.code_file
        if not code_file or not os.path.exists(code_file):
            return False

        input_data = test_case["input_widget"].get("1.0", tk.END).strip()
        expected_output = test_case["output_widget"].get("1.0", tk.END).strip()

        try:
            result = run_python_test(code_file, input_data)

            actual_output_widget = test_case["actual_output_widget"]
            result_frame = test_case["result_frame"]

            # ウィジェットはUIスレッドで操作する
            def update_ui():
                actual_output_widget.config(state="normal")
                actual_output_widget.delete("1.0", tk.END)
                actual_output_widget.insert(tk.END, result["output"])

                passed = compare_outputs(result["output"], expected_output)

                result_frame.set_result(passed)

                if result["error"]:
                    actual_output_widget.insert(
                        tk.END, f"\n\n--- エラー出力 ---\n{result['error']}"
                    )

            self.app_controller.root.after(0, update_ui)

            passed = compare_outputs(result["output"], expected_output)

            # 処理が完了するまで少し待機して、UIの更新が反映されるようにする
            time.sleep(0.1)

            return passed

        except Exception as e:
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

            self.app_controller.root.after(0, show_error)
            return False
