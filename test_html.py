import os
import re
import pytest
from bs4 import BeautifulSoup

# Directory to search for HTML files
REPO_ROOT = os.getcwd()

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
    """Validate HTML syntax using BeautifulSoup."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")

        # Check for unclosed tags
        if soup.find_all(string=lambda text: "unclosed" in text.lower()):
            pytest.fail(f"Unclosed tag detected in file {file_path}")

        # Additional validations can be added here
    except Exception as e:
        pytest.fail(f"HTML syntax error in file {file_path}: {str(e)}")

def validate_hex_colors(file_path):
    """Check HEX color codes in the file to ensure they are valid."""
    hex_pattern = r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Extract all style attributes
            styles = re.findall(r'style="([^"]*)"', content)
            for style in styles:
                matches = re.findall(hex_pattern, style)
                if not matches:
                    pytest.fail(f"Invalid HEX color in {file_path}: {style}")
    except Exception as e:
        pytest.fail(f"Error checking HEX colors in {file_path}: {str(e)}")

@pytest.mark.parametrize("html_file", get_html_files())
def test_html_files(html_file):
    """Test each HTML file for syntax and HEX color correctness."""
    validate_html(html_file)
    validate_hex_colors(html_file)
    
