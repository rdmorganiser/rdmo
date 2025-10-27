from rdmo.projects.imports import Import
from rdmo.projects.models import Project


class TestImportPlugin(Import):
    accept = {"text/plain": [".txt"]}

    def check(self) -> bool:
        # Approve files ending with .txt
        return str(self.file_name).endswith(".txt")

    def process(self):
        # Create a new Project for testing.  You could populate values/tasks/etc.
        self.project = Project(title="Imported test project")
