import json

import pytest

from django.core.management import call_command

import yaml


def test_makemigrations_has_no_changes(db, capsys):
    call_command("makemigrations", check=True, dry_run=True)
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out

@pytest.fixture(scope="session")
def package_json():
    with open("package.json") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def pre_commit_config():
    with open(".pre-commit-config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def package_json_versions(package_json):
    versions = {
        "eslint": package_json["devDependencies"]["eslint"],
        "eslint-plugin-react": package_json["devDependencies"]["eslint-plugin-react"],
        "react": package_json["dependencies"]["react"],
    }
    return {name: version.replace("^", "") for name, version in versions.items()}

@pytest.fixture(scope="session")
def pre_commit_config_versions(pre_commit_config):
    mirrors_eslint = "https://github.com/pre-commit/mirrors-eslint"
    for repo in pre_commit_config["repos"]:
        if repo["repo"] == mirrors_eslint:
            eslint_config = repo["hooks"][0]
            break
    versions = {}
    for dependency in sorted(eslint_config["additional_dependencies"]):
        name, version = dependency.split("@")
        versions[name] = version
    return versions

def test_package_json_and_pre_commit_versions_match(package_json_versions, pre_commit_config_versions):
    assert package_json_versions == pre_commit_config_versions
