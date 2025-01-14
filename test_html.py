import subprocess
import pytest
import re
from pathlib import Path
from bs4 import BeautifulSoup

# List of standard HTML tags for validation
STANDARD_HTML_TAGS = {
    'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'script', 'noscript', 'body',
    'section', 'nav', 'article', 'aside', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'footer',
    'address', 'p', 'hr', 'pre', 'blockquote', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure',
    'figcaption', 'div', 'main', 'a', 'em', 'strong', 'small', 'cite', 'q', 'dfn', 'abbr', 'data',
    'time', 'code', 'var', 'samp', 'kbd', 'sub', 'sup', 'i', 'b', 'u', 'mark', 'ruby', 'rt', 'rp',
    'bdi', 'bdo', 'span', 'br', 'wbr', 'ins', 'del', 'img', 'iframe', 'embed', 'object', 'param',
    'video', 'audio', 'source', 'track', 'canvas', 'map', 'area', 'svg', 'math', 'table', 'caption',
    'colgroup', 'col', 'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'form', 'fieldset', 'legend',
    'label', 'input', 'button', 'select', 'datalist', 'optgroup', 'option', 'textarea', 'keygen',
    'output', 'progress', 'meter', 'details', 'summary', 'menuitem', 'menu'
}

# Helper function to load HTML content
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Get changed HTML files from the PR using git diff
def get_changed_html_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            stdout=subprocess.PIPE,
            check=True,
            text=True
        )
        files = result.stdout.strip().split('\n')
        return [Path(f) for f in files if f.endswith(".html")]
    except subprocess.CalledProcessError:
        return []

# Validate hex color codes in HTML files
def find_invalid_hex_colors(html_content):
    hex_color_pattern = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}(?![0-9a-fA-F])')
    invalid_pattern = re.compile(r"#(?![0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b)[^\s;'\"']+")
    
    valid_colors = set(hex_color_pattern.findall(html_content))
    invalid_colors = set(invalid_pattern.findall(html_content)) - valid_colors
    return list(invalid_colors)

# Detect invalid HTML tags
def find_invalid_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = {tag.name for tag in soup.find_all()}
    invalid_tags = tags - STANDARD_HTML_TAGS
    return list(invalid_tags)

# Detect mismatched HTML tags
def find_mismatched_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tag_stack = []
    mismatches = []
    for tag in soup.find_all(True):
        if not tag.is_self_closing:
            if tag.name not in STANDARD_HTML_TAGS:
                continue
            if tag.name in tag_stack:
                tag_stack.remove(tag.name)
            else:
                tag_stack.append(tag.name)
    if tag_stack:
        mismatches.extend(tag_stack)
    return mismatches

# Collect changed HTML files
changed_html_files = get_changed_html_files()

@pytest.mark.parametrize("html_file", changed_html_files)
def test_html_syntax(html_file):
    try:
        content = load_html(html_file)
        BeautifulSoup(content, 'lxml')  # Stricter parsing for detecting unclosed tags
    except Exception as exc:
        pytest.fail(f"Syntax error in {html_file}: {exc}")

@pytest.mark.parametrize("html_file", changed_html_files)
def test_invalid_hex_colors(html_file):
    content = load_html(html_file)
    invalid_colors = find_invalid_hex_colors(content)
    assert not invalid_colors, f"Invalid hex color codes in {html_file}: {invalid_colors}"

@pytest.mark.parametrize("html_file", changed_html_files)
def test_invalid_html_tags(html_file):
    content = load_html(html_file)
    invalid_tags = find_invalid_html_tags(content)
    assert not invalid_tags, f"Invalid or non-standard HTML tags in {html_file}: {invalid_tags}"

@pytest.mark.parametrize("html_file", changed_html_files)
def test_mismatched_tags(html_file):
    content = load_html(html_file)
    mismatched_tags = find_mismatched_tags(content)
    assert not mismatched_tags, f"Mismatched or unclosed HTML tags in {html_file}: {mismatched_tags}"

if __name__ == "__main__":
    pytest.main()
