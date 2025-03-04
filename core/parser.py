from bs4 import BeautifulSoup
import re


def parse_problem_html(html_content):
    """HTMLの解析処理"""
    # HTMLの解析
    soup = BeautifulSoup(html_content, "html.parser")

    # 問題情報の初期化
    problem_info = {
        "problem_id": "",
        "problem_title": "",
        "contest_number": "",
        "test_cases": [],
    }

    # 問題情報の取得
    task_title = soup.select_one("span.h2")
    if task_title:
        title_text = task_title.get_text().strip()
        match = re.search(r"([A-G]) - (.+)", title_text)
        if match:
            problem_info["problem_id"] = match.group(1)
            problem_info["problem_title"] = match.group(2)

    # コンテスト番号の取得
    contest_url = soup.select_one('a[href^="/contests/"]')
    if contest_url:
        href = contest_url.get("href", "")
        match = re.search(r"/contests/([^/]+)", href)
        if match:
            contest_id = match.group(1)
            if contest_id.startswith("abc"):
                problem_info["contest_number"] = contest_id[3:]  # 'abc395' -> '395'

    # 入力例と出力例の抽出
    sample_sections = soup.select("div.part")

    input_samples = []
    output_samples = []

    for section in sample_sections:
        section_title = section.select_one("h3")
        if not section_title:
            continue

        title_text = section_title.get_text()
        pre_tag = section.select_one("pre")

        if not pre_tag:
            continue

        sample_text = pre_tag.get_text()

        if "入力例" in title_text:
            input_samples.append((title_text, sample_text))
        elif "出力例" in title_text:
            output_samples.append((title_text, sample_text))

    # テストケースとして保存
    for i in range(min(len(input_samples), len(output_samples))):
        # Copyを削除したラベル
        input_title = input_samples[i][0].replace("Copy", "").strip()
        output_title = output_samples[i][0].replace("Copy", "").strip()

        problem_info["test_cases"].append(
            {
                "input_title": input_title,
                "input": input_samples[i][1],
                "output_title": output_title,
                "expected_output": output_samples[i][1],
            }
        )

    return problem_info
