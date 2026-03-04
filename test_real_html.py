#!/usr/bin/env python3
"""実際のAtCoderHTMLでのテスト"""

import sys
sys.path.append('.')

from core.parser import parse_problem_html
from core.input_analysis.input_analyzer import InputAnalyzer

def test_real_html():
    # 実際のHTMLから「X Y」の部分を抜き出してテスト
    html_content = '''
<div class="part">
<section>
<h3>入力</h3><p>入力は以下の形式で標準入力から与えられる。</p>
<pre>X Y</pre>
</section>
</div>

<div class="part">
<section>
<h3>入力例 1</h3>
<pre>1 1</pre>
</section>
</div>

<div class="part">
<section>
<h3>出力例 1</h3>
<pre>415</pre>
</section>
</div>

<div class="part">
<section>
<h3>入力例 2</h3>
<pre>3 7</pre>
</section>
</div>

<div class="part">
<section>
<h3>出力例 2</h3>
<pre>895</pre>
</section>
</div>
    '''

    print("実際のHTMLを使った解析テスト")
    print("=" * 50)

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
    test_real_html()