import subprocess
import pytest
import re
from pathlib import Path
from bs4 import BeautifulSoup

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
    invalid_pattern = re.compile(r'#(?![0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b)[^\s;'"]+')
    
    valid_colors = set(hex_color_pattern.findall(html_content))
    invalid_colors = set(invalid_pattern.findall(html_content)) - valid_colors
    return list(invalid_colors)

# Collect changed HTML files
changed_html_files = get_changed_html_files()

@pytest.mark.parametrize("html_file", changed_html_files)
def test_html_syntax(html_file):
    try:
        content = load_html(html_file)
        BeautifulSoup(content, 'html.parser')
    except Exception as exc:
        pytest.fail(f"Syntax error in {html_file}: {exc}")

@pytest.mark.parametrize("html_file", changed_html_files)
def test_invalid_hex_colors(html_file):
    content = load_html(html_file)
    invalid_colors = find_invalid_hex_colors(content)
    assert not invalid_colors, f"Invalid hex color codes in {html_file}: {invalid_colors}"

if __name__ == "__main__":
    pytest.main()
