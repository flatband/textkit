import re
from html import unescape

_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
_LINK_RE = re.compile(r'<a\b[^>]*\bhref=["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.I | re.S)
_BR_RE = re.compile(r"<br\s*/?>", re.I)
_BLOCK_RE = re.compile(r"</?(p|div|h[1-6])\b[^>]*>", re.I)
_LINE_RE = re.compile(r"<(li|tr|td|th)\b[^>]*>", re.I)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_scripts_and_styles(html_body):
    return _SCRIPT_STYLE_RE.sub("", html_body)


def _inline_links(html_body):
    return _LINK_RE.sub(lambda m: f"{_TAG_RE.sub('', m.group(2))} ({m.group(1)})", html_body)


def _insert_line_breaks(html_body):
    html_body = _BR_RE.sub("\n", html_body)
    html_body = _BLOCK_RE.sub("\n\n", html_body)
    html_body = _LINE_RE.sub("\n", html_body)
    return html_body


def _strip_tags(html_body):
    return _TAG_RE.sub("", html_body)


def _normalize_whitespace(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_to_text(html_body: str) -> str:
    body = _strip_scripts_and_styles(html_body)
    body = _inline_links(body)
    body = _insert_line_breaks(body)
    body = _strip_tags(body)
    body = unescape(body)
    body = _normalize_whitespace(body)
    return body or "This email requires an HTML-compatible client."
