from rdmo.projects.exports import RDMOSnapshotXMLExport


class SimpleSnapshotExportPlugin(RDMOSnapshotXMLExport):
    default_uri_prefix = "https://rdmorganiser.github.io/terms"
