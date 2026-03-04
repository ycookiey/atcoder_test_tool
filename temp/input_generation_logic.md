# AtCoder入力自動生成ロジック

## 概要
AtCoderの問題文から入力形式を解析し、適切な入力処理コードを自動生成するシステム。

## 主要コンポーネント

### 1. `codegen.py` - メインエントリーポイント
- **機能**: 全体の処理フローを制御
- **核心ロジック**:
  ```python
  def generate_code(atcoder_client, problem_url, config, output_file):
      # 1. 問題データ取得
      content = atcoder_client.download_problem_content(problem)

      # 2. 定数予測（MOD値、YES/NO文字列など）
      constants = predict_constants(content.original_html)

      # 3. 入力形式予測
      prediction_result = predict_format(content, constants.is_format_analysis_allowed_by_rule)

      # 4. コード生成
      code_generator(CodeGenArgs(template, prediction_result.format, constants, config))
  ```

### 2. `predict_format.py` - 入力形式予測
- **機能**: HTML問題文から入力形式を解析・予測
- **核心ロジック**:
  ```python
  def predict_format(content, is_format_analysis_allowed_by_rule):
      # 入力形式とサンプルを取得
      input_format = content.get_input_format()
      samples = content.get_samples()

      # 可能な形式パターンを探索
      tokenized_possible_formats = search_formats_with_minimum_vars(input_format)

      # 各パターンで型予測を実行
      for format in tokenized_possible_formats:
          simple_format = predict_simple_format(format.var_tokens, to_1d_flag)
          typed_format = predict_types(simple_format, samples)
  ```

### 3. `predict_types.py` - データ型予測
- **機能**: サンプルデータから変数の型を推論
- **核心ロジック**:
  ```python
  def predict_types(simple_format, samples):
      for sample in samples:
          token_manager = TokenManager(sample.get_input().split())
          predictor = TypePredictor(simple_format)

          # トークンを順次処理して型を推論
          while not token_manager.is_terminal():
              predictor.feed(token_manager.next())
  ```

### 4. `template_engine.py` - テンプレートエンジン
- **機能**: 予測結果をテンプレートに適用してコード生成
- **特徴**:
  - Jinja2テンプレートエンジン使用
  - 旧形式`${}`も後方互換性でサポート
  - 自動インデント調整

### 5. `tokenize_format.py` - 入力形式トークン化
- **機能**: 入力形式文字列を解析可能な形式に変換
- **処理**: パターンマッチングで変数とループ構造を特定

## 処理フロー

1. **問題URL解析** → 問題IDとコンテストIDを抽出
2. **HTML取得・解析** → 入力形式・サンプルデータ・制約を抽出
3. **形式予測** → 入力形式の構造パターンを特定
4. **型推論** → サンプルデータから各変数の型を推論
5. **コード生成** → テンプレートエンジンで最終的な入力処理コードを出力

## 主要クラス・関数

- `TypePredictor`: サンプルデータから型を推論するクラス
- `predict_format()`: 入力形式の全体予測を行う関数
- `search_formats_with_minimum_vars()`: 最小変数数の形式を探索
- `render()`: テンプレートエンジンでのコード生成

## 導入時の注意点

1. **依存関係**: Jinja2, BeautifulSoup4などのライブラリが必要
2. **エラーハンドリング**: 予測失敗時の適切なフォールバック処理
3. **テンプレート設計**: 各言語に対応したテンプレートファイル
4. **サンプル解析**: 不正なサンプルデータに対する堅牢性