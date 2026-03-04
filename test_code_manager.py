#!/usr/bin/env python3
"""パーサーと入力解析を使った統合テスト"""

import sys
sys.path.append('.')

from core.parser import parse_problem_html
from core.input_analysis.input_analyzer import InputAnalyzer

def test_integration():
    print("パーサーと入力解析を使った統合テスト")
    print("=" * 50)

    # HTMLファイルを読み込み
    with open('421B.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # HTMLから問題情報を解析
    problem_info = parse_problem_html(html_content)

    print(f"入力形式: '{problem_info['input_format']}'")

    # 入力解析を実行
    analyzer = InputAnalyzer()
    prediction_result = analyzer.analyze_input_format(
        problem_info['input_format'],
        problem_info['samples']
    )

    if prediction_result:
        print("解析成功!")
        # コード生成
        generated_code = analyzer.generate_python_code(prediction_result)

        # 基本的なテンプレート作成
        full_template = f"""import bisect,collections,copy,heapq,itertools,math,numpy,string
import sys
def I(): return int(sys.stdin.readline().rstrip())
def LI(): return list(map(int,sys.stdin.readline().rstrip().split()))
def S(): return sys.stdin.readline().rstrip()
def LS(): return list(sys.stdin.readline().rstrip().split())

{generated_code}"""

        print("生成されたコード:")
        print(full_template)

        # 新しいファイルに書き込み
        filename = "421B_new.py"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_template)
        print(f"\n{filename} に書き込み完了")
    else:
        print("解析失敗")

if __name__ == "__main__":
    test_integration()