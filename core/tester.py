import subprocess


def run_python_test(code_file, input_data, timeout=5):
    """指定されたPythonファイルで入力データを実行し、結果を返す"""
    process = None
    try:
        process = subprocess.Popen(
            ["python", code_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(input=input_data, timeout=timeout)

        actual_output = stdout.strip()

        return {
            "output": actual_output,
            "error": stderr,
            "success": process.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        if process:
            process.kill()
            stdout, stderr = process.communicate()
        return {
            "output": "Timeout: プログラムの実行が長すぎます",
            "error": "タイムアウトにより強制終了されました",
            "success": False,
        }
    except Exception as e:
        if process and process.poll() is None:
            process.kill()
        return {"output": "", "error": str(e), "success": False}


def compare_outputs(actual, expected):
    """実際の出力と期待される出力を比較（大文字小文字を区別しない）"""
    return actual.lower() == expected.lower()
