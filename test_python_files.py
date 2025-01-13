import subprocess
import pytest
from pathlib import Path

# Get changed Python files from the PR using git diff
def get_changed_python_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            stdout=subprocess.PIPE,
            check=True,
            text=True
        )
        files = result.stdout.strip().split('\n')
        return [Path(f) for f in files if f.endswith(".py")]
    except subprocess.CalledProcessError:
        return []

# Collect only changed Python files
changed_python_files = get_changed_python_files()

@pytest.mark.parametrize("file_path", changed_python_files)
def test_python_syntax(file_path):
    """Test to ensure Python files have correct syntax."""
    with open(file_path, "r") as f:
        code = f.read()
    try:
        compile(code, str(file_path), "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in Python file {file_path}: {e}")

if __name__ == "__main__":
    pytest.main()
