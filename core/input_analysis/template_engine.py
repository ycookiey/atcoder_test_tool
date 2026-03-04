import re
from jinja2 import Environment


def render(template, **kwargs):
    """Jinja2テンプレートエンジンでコードを生成"""
    return render_by_jinja(template, **kwargs)


def render_by_jinja(template, **kwargs):
    return Environment(trim_blocks=True,
                       lstrip_blocks=True).from_string(template).render(**kwargs) + "\n"


def estimate_indent(code):
    indents = re.findall(r'^([ \t]+)(?=\S)', code, re.MULTILINE)
    if not indents:
        return ''
    indents_concat = "".join(indents)
    if ' ' in indents_concat and '\t' in indents_concat:
        return ''
    lens = set([len(indent) for indent in indents])
    if not min(lens) * len(lens) == max(lens):
        return ''
    return indents[0][:min(lens)]
