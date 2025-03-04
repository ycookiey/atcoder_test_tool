import subprocess


# tester.py の変更
def run_python_test(code_file, input_data, timeout=5):
    """指定されたPythonファイルで入力データを実行し、結果を返す"""
    process = None
    try:
        # Pythonプロセスを実行
        process = subprocess.Popen(
            ["python", code_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # タイムアウトを設定して入力データを渡す
        stdout, stderr = process.communicate(input=input_data, timeout=timeout)

        # 出力を整形
        actual_output = stdout.strip()

        return {
            "output": actual_output,
            "error": stderr,
            "success": process.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        # タイムアウトした場合、プロセスを強制終了
        if process:
            process.kill()
            stdout, stderr = process.communicate()
        return {
            "output": "Timeout: プログラムの実行が長すぎます",
            "error": "タイムアウトにより強制終了されました",
            "success": False,
        }
    except Exception as e:
        # その他のエラーが発生した場合もプロセスを終了
        if process and process.poll() is None:
            process.kill()
        return {"output": "", "error": str(e), "success": False}


def compare_outputs(actual, expected):
    """実際の出力と期待される出力を比較（大文字小文字を区別しない）"""
    return actual.lower() == expected.lower()
