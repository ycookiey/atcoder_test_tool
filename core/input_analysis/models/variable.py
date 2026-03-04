from typing import Optional


class Index:
    """変数のインデックス情報を管理するクラス"""

    def __init__(self, min_index=None, max_index=None):
        self.min_index = min_index
        self.max_index = max_index

    def evaluate(self, var_dict):
        """インデックスの値を評価"""
        if self.min_index is not None:
            min_val = self.min_index.evaluate(var_dict) if hasattr(self.min_index, 'evaluate') else self.min_index
        else:
            min_val = None

        if self.max_index is not None:
            max_val = self.max_index.evaluate(var_dict) if hasattr(self.max_index, 'evaluate') else self.max_index
        else:
            max_val = None

        return min_val, max_val


class SimpleVariable:
    """シンプルな変数情報を管理するクラス"""

    def __init__(self, name: str, first_index: Optional[Index] = None, second_index: Optional[Index] = None):
        self.name = name
        self.first_index = first_index
        self.second_index = second_index

    def is_array(self) -> bool:
        """配列変数かどうか"""
        return self.first_index is not None

    def is_2d_array(self) -> bool:
        """2次元配列かどうか"""
        return self.first_index is not None and self.second_index is not None

    def __str__(self):
        if self.is_2d_array():
            return f"{self.name}[{self.first_index}][{self.second_index}]"
        elif self.is_array():
            return f"{self.name}[{self.first_index}]"
        else:
            return self.name

    def __repr__(self):
        return f"SimpleVariable(name='{self.name}', first_index={self.first_index}, second_index={self.second_index})"


class VariableToken:
    """変数トークン（入力形式解析用）"""

    def __init__(self, var_name: str, first_index: Optional[str] = None, second_index: Optional[str] = None):
        self.var_name = var_name
        self.first_index = first_index
        self.second_index = second_index

    def is_valid(self) -> bool:
        """トークンが有効かどうか"""
        if not self.var_name:
            return False
        return True

    def dim_num(self) -> int:
        """次元数を返す"""
        if self.second_index is not None:
            return 2
        elif self.first_index is not None:
            return 1
        else:
            return 0

    def __str__(self):
        if self.second_index:
            return f"{self.var_name}_{self.first_index}_{self.second_index}"
        elif self.first_index:
            return f"{self.var_name}_{self.first_index}"
        else:
            return self.var_name


class TokenizedFormat:
    """トークン化された入力形式"""

    def __init__(self, var_tokens):
        self.var_tokens = var_tokens

    def __str__(self):
        return " ".join(str(token) for token in self.var_tokens)