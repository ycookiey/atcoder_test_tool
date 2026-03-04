#!/usr/bin/env python3
"""X Y 入力形式のデバッグ"""

import sys
sys.path.append('.')

from core.input_analysis.input_analyzer import InputAnalyzer
from core.input_analysis.models.sample import Sample

def test_xy_format():
    print("X Y 形式のデバッグテスト")
    print("=" * 50)

    analyzer = InputAnalyzer()

    # テストデータ
    input_format = "X Y"
    samples = [
        Sample("1 2", ""),
        Sample("3 4", ""),
        Sample("5 6", "")
    ]

    print(f"入力形式: '{input_format}'")
    for i, sample in enumerate(samples):
        print(f"サンプル{i+1}: '{sample.get_input()}'")

    print("\n解析開始...")
    prediction_result = analyzer.analyze_input_format(input_format, samples)

    if prediction_result:
        print("解析成功!")
        variables = prediction_result.format.get_variables()
        print(f"変数数: {len(variables)}")
        for i, var in enumerate(variables):
            print(f"変数{i+1}: name='{var.name}', is_array={var.is_array()}")

        print("\n生成されたコード:")
        generated_code = analyzer.generate_python_code(prediction_result)
        print(generated_code)
    else:
        print("解析失敗")

    status = analyzer.get_analysis_status_message()
    print(f"\nステータス: {status}")

if __name__ == "__main__":
    test_xy_format()