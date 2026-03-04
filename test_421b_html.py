#!/usr/bin/env python3
"""421B.htmlを使った実際のテスト"""

import sys
sys.path.append('.')

from core.parser import parse_problem_html
from core.input_analysis.input_analyzer import InputAnalyzer

def test_421b_html():
    print("421B.html を使った実際のテスト")
    print("=" * 50)

    # HTMLファイルを読み込み
    with open('421B.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # HTMLを解析
    result = parse_problem_html(html_content)

    print(f"入力形式: '{result['input_format']}'")
    print(f"サンプル数: {len(result['samples'])}")

    for i, sample in enumerate(result['samples']):
        print(f"サンプル{i+1}: '{sample.get_input()}' -> '{sample.get_output()}'")

    print("\n入力解析テスト:")

    analyzer = InputAnalyzer()
    prediction_result = analyzer.analyze_input_format(
        result['input_format'],
        result['samples']
    )

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
    test_421b_html()