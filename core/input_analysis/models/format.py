from typing import List, Generic, TypeVar, Optional
from .variable import SimpleVariable

T = TypeVar('T')


class Pattern:
    """入力パターンの基底クラス"""
    pass


class SingularPattern(Pattern):
    """単一変数のパターン"""

    def __init__(self, var: SimpleVariable):
        self.var = var

    def __str__(self):
        return str(self.var)


class ParallelPattern(Pattern):
    """並列パターン（同じ行に複数の変数）"""

    def __init__(self, vars: List[SimpleVariable], loop_index=None):
        self.vars = vars
        self.loop_index = loop_index

    def __str__(self):
        return " ".join(str(var) for var in self.vars)


class TwoDimensionalPattern(Pattern):
    """2次元パターン"""

    def __init__(self, var: SimpleVariable):
        self.var = var

    def __str__(self):
        return str(self.var)


class Format(Generic[T]):
    """入力形式を表現するクラス"""

    def __init__(self, sequence: List[Pattern]):
        self.sequence = sequence

    def is_empty(self) -> bool:
        """空の形式かどうか"""
        return len(self.sequence) == 0

    def get_variables(self) -> List[SimpleVariable]:
        """すべての変数を取得"""
        variables = []
        for pattern in self.sequence:
            if isinstance(pattern, SingularPattern):
                variables.append(pattern.var)
            elif isinstance(pattern, ParallelPattern):
                variables.extend(pattern.vars)
            elif isinstance(pattern, TwoDimensionalPattern):
                variables.append(pattern.var)
        return variables

    def __str__(self):
        return "\n".join(str(pattern) for pattern in self.sequence)


class FormatPredictionResult:
    """形式予測の結果"""

    def __init__(self, format_obj: Optional[Format] = None, prediction_success: bool = False):
        self.format = format_obj if format_obj else Format([])
        self.prediction_success = prediction_success

    @staticmethod
    def empty_result():
        """空の結果を作成"""
        return FormatPredictionResult(Format([]), False)

    @staticmethod
    def create_typed_format(simple_format: Format, type_dict: dict):
        """型付きフォーマットを作成"""
        # TODO: 型情報を simple_format に統合する処理
        return FormatPredictionResult(simple_format, True)

    def is_successful(self) -> bool:
        """予測が成功したかどうか"""
        return self.prediction_success