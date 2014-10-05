import re

from django.utils.html import strip_spaces_between_tags

RE_MULTISPACE = re.compile(r"\s{2,}")
RE_NEWLINE = re.compile(r"\n")


def strip_spaces_from_html(html):
    stripped = strip_spaces_between_tags(html.strip())
    stripped = RE_MULTISPACE.sub(" ", stripped)
    stripped = RE_NEWLINE.sub("", stripped)
    return stripped
