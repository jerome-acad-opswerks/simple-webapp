import subprocess
import pytest
import os
from bs4 import BeautifulSoup
from lxml import etree
import re

REPO_ROOT = os.getcwd()

def get_html_files():
    html_files = []
    for root, _, files in os.walk(REPO_ROOT):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def validate_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        parser = etree.HTMLParser(recover=False)
        etree.fromstring(content, parser)
        print(f"{file_path} is well-formed.")
    except etree.XMLSyntaxError as e:
        pytest.fail(f"HTML syntax error in file {file_path}: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error in {file_path}: {str(e)}")

def validate_hex_colors(file_path):
    hex_pattern = r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        styles = re.findall(r'style="([^"]*)"', content)
        for style in styles:
            matches = re.findall(hex_pattern, style)
            if not matches and "color" in style:
                pytest.fail(f"Invalid HEX color in {file_path}: {style}")
    except Exception as e:
        pytest.fail(f"Error checking HEX colors in {file_path}: {str(e)}")

def detect_changed_html_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        changed_files = result.stdout.splitlines()
        return [file for file in changed_files if file.endswith(".html")]
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e.stderr}")
        return []

def run_tests_if_html_changed():
    html_files = detect_changed_html_files()
    if html_files:
        print(f"HTML files changed: {html_files}")
        for html_file in html_files:
            validate_html(html_file)
            validate_hex_colors(html_file)
    else:
        print("No HTML files changed. Skipping tests.")

if __name__ == "__main__":
    run_tests_if_html_changed()
