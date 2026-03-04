class TokenManager:
    """トークンの管理を行うクラス"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        """現在のトークンを確認（位置は進めない）"""
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def next(self):
        """次のトークンを取得"""
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token
        return None

    def go_next(self):
        """位置を次に進める"""
        self.index += 1

    def go_back(self):
        """位置を前に戻す"""
        if self.index > 0:
            self.index -= 1

    def is_terminal(self):
        """終端に達したかどうか"""
        return self.index >= len(self.tokens)