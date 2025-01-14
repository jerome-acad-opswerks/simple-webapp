import os
import re
import pytest
from html5lib import parse

def get_changed_files():
    """
    Retrieve a list of changed HTML files in the current Pull Request.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.splitlines()
        return [f for f in files if f.endswith(".html")]
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to retrieve changed files: {str(e)}")

def validate_html(file_path):
    """Parse the HTML file to ensure it is syntactically valid."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            # Parse the HTML content
            parse(html_content, treebuilder="dom")
    except Exception as e:
        pytest.fail(f"HTML syntax error in file {file_path}: {str(e)}")

@pytest.mark.parametrize("html_file", get_changed_files())
def test_html_syntax(html_file):
    """Test each modified HTML file for syntax correctness."""
    validate_html(html_file)

def test_hex_color_in_index_html():
    """Test if the HEX color in index.html is valid."""
    # Path to the specific file
    file_path = "path/to/index.html"
    if not os.path.exists(file_path):
        pytest.fail(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regular expression to find HEX colors
    hex_pattern = r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})"
    matches = re.findall(hex_pattern, content)

    if not matches:
        pytest.fail("No valid HEX color found in the file.")

    for hex_color in matches:
        if not re.match(r"^#[0-9a-fA-F]{6}$", hex_color):
            pytest.fail(f"Invalid HEX color: {hex_color}")

    # Test passes if all HEX colors are valid
