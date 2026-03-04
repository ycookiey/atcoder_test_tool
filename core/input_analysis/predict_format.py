from .models.sample import Sample
from .predict_simple_format import predict_simple_format, SimpleFormatPredictionFailedError
from .tokenize_format import NoFormatFoundError, search_formats_with_minimum_vars
from .predict_types import predict_types, TypePredictionFailedError
from .models.format import FormatPredictionResult


class NoPredictionResultError(Exception):
    pass


class MultiplePredictionResultsError(Exception):

    def __init__(self, cands):
        self.cands = cands


class PredictionNotAllowedError(Exception):
    pass


def predict_format(input_format: str, samples: list, is_format_analysis_allowed_by_rule: bool) -> FormatPredictionResult:
    if not is_format_analysis_allowed_by_rule:
        raise PredictionNotAllowedError

    if len(samples) == 0:
        raise NoPredictionResultError

    if not input_format or input_format.strip() == "":
        raise NoPredictionResultError

    try:
        tokenized_possible_formats = search_formats_with_minimum_vars(input_format)
    except NoFormatFoundError:
        raise NoPredictionResultError

    output_cands = []
    for format in tokenized_possible_formats:
        for to_1d_flag in [False, True]:
            try:
                simple_format = predict_simple_format(
                    format.var_tokens, to_1d_flag)
                output_cands.append(
                    FormatPredictionResult.create_typed_format(simple_format, predict_types(simple_format, samples)))
                break
            except (TypePredictionFailedError, SimpleFormatPredictionFailedError):
                pass

    if len(output_cands) > 1:
        raise MultiplePredictionResultsError(output_cands)
    if len(output_cands) == 0:
        raise NoPredictionResultError
    return output_cands[0]
