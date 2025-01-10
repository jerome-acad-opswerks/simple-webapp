import os
import pytest
import yaml
from pathlib import Path

# Directory containing Kubernetes YAML files
K8S_YAML_DIR = Path("./")

# Helper function to load YAML files
def load_yaml(file_path):
    with open(file_path, 'r') as stream:
        return list(yaml.safe_load_all(stream))

# Collect all YAML files in the directory
def find_yaml_files(directory):
    return [file for file in directory.rglob("*.yaml")] + [file for file in directory.rglob("*.yml")]

# Pytest to validate YAML syntax
@pytest.mark.parametrize("yaml_file", find_yaml_files(K8S_YAML_DIR))
def test_yaml_syntax(yaml_file):
    try:
        docs = load_yaml(yaml_file)
        assert docs is not None, f"YAML file {yaml_file} is empty or invalid."
    except yaml.YAMLError as exc:
        pytest.fail(f"Syntax error in {yaml_file}: {exc}")

# Pytest to check required Kubernetes fields
@pytest.mark.parametrize("yaml_file", find_yaml_files(K8S_YAML_DIR))
def test_k8s_required_fields(yaml_file):
    required_fields = ["apiVersion", "kind", "metadata"]
    docs = load_yaml(yaml_file)
    for doc in docs:
        for field in required_fields:
            assert field in doc, f"Missing '{field}' in {yaml_file}"
        assert "name" in doc["metadata"], f"Missing 'metadata.name' in {yaml_file}"

if __name__ == "__main__":
    pytest.main()
