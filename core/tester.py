import subprocess


def run_python_test(code_file, input_data):
    """指定されたPythonファイルで入力データを実行し、結果を返す"""
    try:
        # Pythonプロセスを実行
        process = subprocess.Popen(
            ["python", code_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 入力データを渡す
        stdout, stderr = process.communicate(input=input_data)

        # 出力を整形
        actual_output = stdout.strip()

        return {
            "output": actual_output,
            "error": stderr,
            "success": process.returncode == 0,
        }

    except Exception as e:
        return {"output": "", "error": str(e), "success": False}


def compare_outputs(actual, expected):
    """実際の出力と期待される出力を比較（大文字小文字を区別しない）"""
    return actual.lower() == expected.lower()
