import subprocess
import pytest
import yaml
from pathlib import Path

# Function to load YAML files
def load_yaml(file_path):
    with open(file_path, 'r') as stream:
        return list(yaml.safe_load_all(stream))

# Get changed YAML files from the PR using git diff
def get_changed_yaml_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            stdout=subprocess.PIPE,
            check=True,
            text=True
        )
        files = result.stdout.strip().split('\n')
        return [Path(f) for f in files if f.endswith((".yaml", ".yml"))]
    except subprocess.CalledProcessError:
        return []

# Collect only changed YAML files
changed_yaml_files = get_changed_yaml_files()

@pytest.mark.parametrize("yaml_file", changed_yaml_files)
def test_yaml_syntax(yaml_file):
    try:
        docs = load_yaml(yaml_file)
        assert docs is not None, f"YAML file {yaml_file} is empty or invalid."
    except yaml.YAMLError as exc:
        pytest.fail(f"Syntax error in {yaml_file}: {exc}")

@pytest.mark.parametrize("yaml_file", changed_yaml_files)
def test_k8s_required_fields(yaml_file):
    required_fields = ["apiVersion", "kind", "metadata"]
    docs = load_yaml(yaml_file)
    for doc in docs:
        for field in required_fields:
            assert field in doc, f"Missing '{field}' in {yaml_file}"
        assert "name" in doc["metadata"], f"Missing 'metadata.name' in {yaml_file}"

if __name__ == "__main__":
    pytest.main()
