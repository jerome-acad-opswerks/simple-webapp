import subprocess
import pytest
import os
from bs4 import BeautifulSoup
import re

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
    """Validate HTML syntax using BeautifulSoup and lxml."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse with lxml's strict parser to catch syntax errors
        parser = etree.HTMLParser(recover=False)  # Set recover=False to not automatically fix errors
        etree.fromstring(content, parser)
        
        # If no error occurs, pass the test
        print(f"{file_path} is well-formed.")

    except etree.XMLSyntaxError as e:
        pytest.fail(f"HTML syntax error in file {file_path}: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error while processing {file_path}: {str(e)}")

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

def detect_changed_html_files():
    """Check for changed HTML files in the current commit or branch."""
    # Get list of changed files between the current and previous commit
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    changed_files = result.stdout.splitlines()
    
    # Filter for HTML files
    html_files = [file for file in changed_files if file.endswith(".html")]
    return html_files

def run_tests_if_html_changed():
    """Run tests if any HTML files are changed."""
    html_files = detect_changed_html_files()
    
    if html_files:
        print(f"HTML files changed: {html_files}")
        for html_file in html_files:
            validate_html(html_file)
            validate_hex_colors(html_file)
        pytest.main()  # Run pytest if there are any HTML changes
    else:
        print("No HTML files changed. Skipping tests.")

if __name__ == "__main__":
    run_tests_if_html_changed()
