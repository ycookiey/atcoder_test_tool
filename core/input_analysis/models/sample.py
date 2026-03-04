class Sample:
    """サンプルデータを管理するクラス"""

    def __init__(self, input_text: str, output_text: str = ""):
        self.input_text = input_text.strip()
        self.output_text = output_text.strip()

    def get_input(self) -> str:
        """入力テキストを取得"""
        return self.input_text

    def get_output(self) -> str:
        """出力テキストを取得"""
        return self.output_text

    def get_input_lines(self) -> list:
        """入力を行ごとに分割"""
        return self.input_text.split('\n') if self.input_text else []

    def __str__(self):
        return f"Input:\n{self.input_text}\nOutput:\n{self.output_text}"

    def __repr__(self):
        return f"Sample(input='{self.input_text[:20]}...', output='{self.output_text[:20]}...')"