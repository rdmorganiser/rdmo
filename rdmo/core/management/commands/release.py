import os
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

import requests

from rdmo import __version__ as VERSION

NAME = 'rdmo'


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            import twine  # noqa: F401
        except ImportError as e:
            raise CommandError('twine is not installed.') from e

        self.check_git_tag()
        self.check_github_release()
        self.check_assets()
        self.check_twine()
        self.upload_pypi_test()
        self.upload_pypi()

    def check_git_tag(self):
        # check if we are on the correct git tag
        git_tag = subprocess.check_output(["git", "describe", "--tags"]).decode().strip()
        if git_tag != VERSION:
            raise CommandError(f"git tag mismatch: {git_tag} != {VERSION}.")

    def check_github_release(self):
        # check that there is a github release for this version
        git_remote_url = (
            subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
                      .decode().strip().replace('.git', '')
        )
        if git_remote_url.startswith("https://github.com"):
            github_url = git_remote_url
        elif git_remote_url.startswith("git@github.com:"):
            github_url = git_remote_url.replace("git@github.com:", "https://github.com/")
        else:
            raise CommandError("could not determine GitHub url.")

        release_url = f"{github_url}/releases/tag/{VERSION}"

        try:
            response = requests.get(release_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise CommandError(f"could not access GitHub release at {release_url}.") from e

    def check_assets(self):
        last_commit_time = float(subprocess.check_output(["git", "log", "-1", "--format=%ct"]).decode().strip())

        for asset_path in [
            Path("dist").joinpath(f"{NAME}-{VERSION}.tar.gz"),
            Path("dist").joinpath(f"{NAME}-{VERSION}-py3-none-any.whl")
        ]:
            # check that the asset exists
            if not asset_path.exists():
                raise CommandError(f"version mismatch: {asset_path} does not exist.")

            # check tarball modification time
            asset_modification_time = os.path.getmtime(asset_path)
            if asset_modification_time < last_commit_time:
                raise CommandError(f"timestamp mismatch: {asset_path} is older than the last commit.")

    def check_twine(self):
        subprocess.check_call(["twine", "check", "dist/*"])

    def upload_pypi_test(self):
        answer = input("Upload to test.pypi.org. Do you want to continue? [y/N]")
        if answer.lower() in ["y", "yes"]:
            subprocess.check_call(["twine", "upload", "-r", "testpypi", "dist/*"])
        else:
            print("Skipping.")

    def upload_pypi(self):
        answer = input("Upload to pypi.org. Do you want to continue? [y/N]")
        if answer.lower() in ["y", "yes"]:
            subprocess.check_call(["twine", "upload", "dist/*"])
        else:
            print("Abort.")
