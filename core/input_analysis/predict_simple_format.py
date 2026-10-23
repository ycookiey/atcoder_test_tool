from .models.format import Format, SingularPattern, ParallelPattern
from .models.variable import SimpleVariable


class SimpleFormatPredictionFailedError(Exception):
    pass


def predict_simple_format(var_tokens, to_1d_flag=False):
    """シンプルなフォーマット予測"""
    try:
        patterns = []

        for token in var_tokens:
            var = SimpleVariable(token.var_name)

            if token.first_index and not token.second_index:
                if to_1d_flag:
                    patterns.append(SingularPattern(var))
                else:
                    patterns.append(SingularPattern(var))
            elif token.first_index and token.second_index:
                patterns.append(SingularPattern(var))
            else:
                patterns.append(SingularPattern(var))

        return Format(patterns)

    except Exception:
        raise SimpleFormatPredictionFailedError