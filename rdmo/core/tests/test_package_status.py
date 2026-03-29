import json

from django.core.management import call_command

import yaml
from packaging.version import Version


def test_makemigrations_has_no_changes(db, capsys):
    call_command("makemigrations", check=True, dry_run=True)
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out


def test_package_json_and_pre_commit_versions_match():
    with open(".pre-commit-config.yaml") as f:
        pre_commit_config = yaml.safe_load(f)

    with open("package.json") as f:
        package_json = json.load(f)

    mirrors_eslint_url = "https://github.com/pre-commit/mirrors-eslint"
    for repo in pre_commit_config["repos"]:
        if repo["repo"] == mirrors_eslint_url:
            eslint_config = repo["hooks"][0]
            break

    pre_commit_config_versions = {}
    for dependency in sorted(eslint_config["additional_dependencies"]):
        name, version = dependency.split("@")
        pre_commit_config_versions[name] = Version(version.lstrip("^~"))

    for name, version in package_json["devDependencies"].items():
        if name in pre_commit_config_versions:
            assert pre_commit_config_versions[name].major == Version(version.strip('^~')).major, name
            assert abs(pre_commit_config_versions[name].minor - Version(version.strip('^~')).minor) < 3
