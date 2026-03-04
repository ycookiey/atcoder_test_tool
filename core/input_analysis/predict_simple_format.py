from .models.format import Format, SingularPattern, ParallelPattern
from .models.variable import SimpleVariable


class SimpleFormatPredictionFailedError(Exception):
    pass


def predict_simple_format(var_tokens, to_1d_flag=False):
    """シンプルなフォーマット予測"""
    try:
        patterns = []

        for token in var_tokens:
            # トークンから SimpleVariable を作成
            var = SimpleVariable(token.var_name)

            # 1次元配列の場合
            if token.first_index and not token.second_index:
                if to_1d_flag:
                    # 1次元配列として扱う
                    patterns.append(SingularPattern(var))
                else:
                    # 通常の変数として扱う
                    patterns.append(SingularPattern(var))
            # 2次元配列の場合
            elif token.first_index and token.second_index:
                patterns.append(SingularPattern(var))
            # 単純な変数の場合
            else:
                patterns.append(SingularPattern(var))

        return Format(patterns)

    except Exception:
        raise SimpleFormatPredictionFailedError