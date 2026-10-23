import re
from typing import List, Dict, Any


class CalcParseError(Exception):
    """計算式の解析エラー"""
    pass


class EvaluateError(Exception):
    """計算式の評価エラー"""
    pass


class CalcNode:
    """計算式のノード"""

    def __init__(self, value=None, operator=None, left=None, right=None):
        self.value = value
        self.operator = operator
        self.left = left
        self.right = right

    @staticmethod
    def parse(expression: str) -> 'CalcNode':
        """式を解析してノードを作成"""
        expression = expression.strip()

        if expression.isdigit():
            return CalcNode(value=int(expression))

        if re.match(r'^[a-zA-Z_]\w*$', expression):
            return CalcNode(value=expression)

        for op in ['+', '-', '*', '/']:
            if op in expression:
                parts = expression.split(op, 1)
                if len(parts) == 2:
                    left = CalcNode.parse(parts[0].strip())
                    right = CalcNode.parse(parts[1].strip())
                    return CalcNode(operator=op, left=left, right=right)

        # 解析できない場合は変数として扱う
        return CalcNode(value=expression)

    def get_all_variables(self) -> List[str]:
        """式に含まれるすべての変数を取得"""
        variables = []

        if self.value is not None:
            if isinstance(self.value, str) and not self.value.isdigit():
                variables.append(self.value)

        if self.left:
            variables.extend(self.left.get_all_variables())

        if self.right:
            variables.extend(self.right.get_all_variables())

        return list(set(variables))

    def evaluate(self, var_dict: Dict[str, Any]) -> Any:
        """式を評価"""
        try:
            if self.value is not None:
                if isinstance(self.value, int):
                    return self.value
                elif isinstance(self.value, str):
                    if self.value.isdigit():
                        return int(self.value)
                    elif self.value in var_dict:
                        return var_dict[self.value]
                    else:
                        raise EvaluateError(f"Unknown variable: {self.value}")

            if self.operator and self.left and self.right:
                left_val = self.left.evaluate(var_dict)
                right_val = self.right.evaluate(var_dict)

                if self.operator == '+':
                    return left_val + right_val
                elif self.operator == '-':
                    return left_val - right_val
                elif self.operator == '*':
                    return left_val * right_val
                elif self.operator == '/':
                    return left_val // right_val

            raise EvaluateError("Invalid expression")

        except Exception as e:
            raise EvaluateError(str(e))