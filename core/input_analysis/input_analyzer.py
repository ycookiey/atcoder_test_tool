"""
AtCoder入力形式自動解析のメインクラス
"""
from typing import List, Optional, Dict, Any
from .models.sample import Sample
from .models.format import FormatPredictionResult
from .predict_format import predict_format, NoPredictionResultError, MultiplePredictionResultsError, PredictionNotAllowedError


class InputAnalyzer:
    """入力形式を解析してPythonコードを生成するクラス"""

    def __init__(self):
        self.last_prediction_result = None
        self.last_generated_code = None

    def analyze_input_format(self, input_format_text: str, samples: List[Sample]) -> Optional[FormatPredictionResult]:
        """
        入力形式を解析する

        Args:
            input_format_text: 問題文の入力形式セクション
            samples: サンプルデータのリスト

        Returns:
            予測結果（失敗時はNone）
        """
        try:
            # 常に解析を許可
            result = predict_format(input_format_text, samples, is_format_analysis_allowed_by_rule=True)
            self.last_prediction_result = result
            return result

        except (NoPredictionResultError, MultiplePredictionResultsError, PredictionNotAllowedError):
            # 解析失敗時は静かに None を返す
            self.last_prediction_result = None
            return None
        except Exception:
            # その他のエラーも静かに処理
            self.last_prediction_result = None
            return None

    def generate_python_code(self, prediction_result: FormatPredictionResult) -> str:
        """
        予測結果からPythonの入力処理コードを生成

        Args:
            prediction_result: 入力形式の予測結果

        Returns:
            生成されたPythonコード
        """
        if not prediction_result or not prediction_result.is_successful():
            return self._generate_fallback_code()

        try:
            code_lines = []
            variables = prediction_result.format.get_variables()

            # TODO: より高度なコード生成ロジックを実装
            # 現在は基本的なパターンのみサポート

            if len(variables) == 1:
                var = variables[0]
                if var.is_array():
                    code_lines.append(f"N = int(input())")
                    code_lines.append(f"{var.name} = list(map(int, input().split()))")
                else:
                    code_lines.append(f"{var.name} = int(input())")
            elif len(variables) == 2:
                var1, var2 = variables[0], variables[1]
                if not var1.is_array() and not var2.is_array():
                    code_lines.append(f"{var1.name}, {var2.name} = map(int, input().split())")
                else:
                    code_lines.append(f"{var1.name} = int(input())")
                    code_lines.append(f"{var2.name} = list(map(int, input().split()))")
            else:
                # 複数変数の場合は基本的なパターンを生成
                if len(variables) <= 4:
                    var_names = [var.name for var in variables if not var.is_array()]
                    if var_names:
                        code_lines.append(f"{', '.join(var_names)} = map(int, input().split())")

                # 配列変数があれば追加
                for var in variables:
                    if var.is_array():
                        code_lines.append(f"{var.name} = list(map(int, input().split()))")

            # コードが生成できなかった場合はフォールバック
            if not code_lines:
                return self._generate_fallback_code()

            # TODO コメントを追加
            code_lines.append("")
            code_lines.append("# TODO: 問題解決のロジックを実装")

            generated_code = "\n".join(code_lines)
            self.last_generated_code = generated_code
            return generated_code

        except Exception:
            return self._generate_fallback_code()

    def _generate_fallback_code(self) -> str:
        """解析失敗時のフォールバックコード"""
        return """# 入力形式の自動解析に失敗しました
# 手動で入力処理を記述してください

# TODO: 入力処理を記述
# 例: N = int(input())

# TODO: 問題解決のロジックを実装"""

    def get_analysis_status_message(self) -> str:
        """解析状況のステータスメッセージを取得"""
        if self.last_prediction_result is None:
            return "入力形式: 手動入力"
        elif self.last_prediction_result.is_successful():
            var_count = len(self.last_prediction_result.format.get_variables())
            return f"入力形式: {var_count}個の変数を検出 (自動生成済み)"
        else:
            return "入力形式: 解析完了"