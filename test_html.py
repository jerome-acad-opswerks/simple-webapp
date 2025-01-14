import os
import re
import pytest
from html5lib import parse

# Directory to search for HTML files
REPO_ROOT = os.getcwd()  # Current directory (repository root)

def get_html_files():
    """
    Retrieve a list of all .html files in the repository.
    """
    html_files = []
    for root, _, files in os.walk(REPO_ROOT):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def validate_html(file_path):
    """Parse the HTML file to ensure it is syntactically valid."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            parse(html_content, treebuilder="dom")  # Validate with html5lib
    except Exception as e:
        pytest.fail(f"HTML syntax error in file {file_path}: {str(e)}")

def validate_hex_colors(file_path):
    """Check HEX color codes in the file to ensure they are valid."""
    hex_pattern = r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(hex_pattern, content)
            if matches:
                for hex_color in matches:
                    if not re.match(r"^#[0-9a-fA-F]{6}$", hex_color):
                        pytest.fail(f"Invalid HEX color in {file_path}: {hex_color}")
    except Exception as e:
        pytest.fail(f"Error checking HEX colors in {file_path}: {str(e)}")

@pytest.mark.parametrize("html_file", get_html_files())
def test_html_files(html_file):
    """Test each HTML file for syntax and HEX color correctness."""
    validate_html(html_file)
    validate_hex_colors(html_file)
