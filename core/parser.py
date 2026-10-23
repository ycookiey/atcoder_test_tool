from bs4 import BeautifulSoup
import re
from .input_analysis.models.sample import Sample


def parse_problem_html(html_content):
    """HTMLの解析処理"""
    soup = BeautifulSoup(html_content, "html.parser")

    problem_info = {
        "problem_id": "",
        "problem_title": "",
        "contest_number": "",
        "test_cases": [],
        "input_format": "",
        "samples": [],
    }

    task_title = soup.select_one("span.h2")
    if task_title:
        title_text = task_title.get_text().strip()
        match = re.search(r"([A-G]) - (.+)", title_text)
        if match:
            problem_info["problem_id"] = match.group(1)
            problem_info["problem_title"] = match.group(2)

    contest_url = soup.select_one('a[href^="/contests/"]')
    if contest_url:
        href = contest_url.get("href", "")
        match = re.search(r"/contests/([^/]+)", href)
        if match:
            contest_id = match.group(1)
            if contest_id.startswith("abc"):
                problem_info["contest_number"] = contest_id[3:]  # 'abc395' -> '395'

    for section in soup.select("div.part"):
        section_title = section.select_one("h3")
        if section_title:
            title_text = section_title.get_text().strip()

            if "入力" in title_text and "例" not in title_text:  # "入力例"を除外
                pre_tag = section.select_one("pre")
                if pre_tag:
                    # KaTeXで描画した数式は、annotationに元のTeXの式が入っている
                    katex_annotations = pre_tag.select("annotation[encoding='application/x-tex']")
                    if katex_annotations:
                        input_format_parts = []
                        for annotation in katex_annotations:
                            input_format_parts.append(annotation.get_text().strip())
                        input_format_text = " ".join(input_format_parts)
                    else:
                        input_format_text = pre_tag.get_text().strip()

                    problem_info["input_format"] = input_format_text
                    break

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

    for i in range(min(len(input_samples), len(output_samples))):
        # h3にはコピーのボタンの文字Copyが入っている
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

    for i in range(min(len(input_samples), len(output_samples))):
        sample = Sample(input_samples[i][1], output_samples[i][1])
        problem_info["samples"].append(sample)

    return problem_info
