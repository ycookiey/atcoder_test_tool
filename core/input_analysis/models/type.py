from enum import Enum
from typing import Optional


class TypeEnum(Enum):
    """データ型の列挙"""
    INT = "int"
    FLOAT = "float"
    STRING = "str"
    UNKNOWN = "unknown"


class Type:
    """変数の型情報を管理するクラス"""

    def __init__(self, type_enum: TypeEnum):
        self.type_enum = type_enum

    @staticmethod
    def from_py_type(py_type) -> 'Type':
        """Pythonの型から Type オブジェクトを作成"""
        if py_type == int:
            return Type(TypeEnum.INT)
        elif py_type == float:
            return Type(TypeEnum.FLOAT)
        elif py_type == str:
            return Type(TypeEnum.STRING)
        else:
            return Type(TypeEnum.UNKNOWN)

    def intersect(self, other: 'Type') -> 'Type':
        """型の交集合を計算（型推論用）"""
        if self.type_enum == other.type_enum:
            return self

        if (self.type_enum == TypeEnum.INT and other.type_enum == TypeEnum.FLOAT) or \
           (self.type_enum == TypeEnum.FLOAT and other.type_enum == TypeEnum.INT):
            return Type(TypeEnum.FLOAT)

        # どの値も表せるstringにそろえる
        return Type(TypeEnum.STRING)

    def to_python_type_name(self) -> str:
        """Python の型名文字列を返す"""
        return self.type_enum.value

    def __str__(self):
        return self.type_enum.value

    def __repr__(self):
        return f"Type({self.type_enum})"

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        return self.type_enum == other.type_enum