import io
import xml.etree.ElementTree as ET
from xml.sax.saxutils import XMLGenerator

from rdmo.projects.renderers import XMLRenderer


def add_memberships_to_xml(xml_path: str, members: list[dict]) -> None:
    """
    Replace or add <memberships> in the given project.xml using the real XMLRenderer.
    `members` is a list of {"role": ..., "user": {...}} dicts.
    """
    # 1) render just the <memberships> fragment with the real renderer
    buf = io.StringIO()
    xml = XMLGenerator(buf, encoding="utf-8")
    xml.startDocument()
    xml.startElement("root", {})                      # wrapper so we can parse as a fragment
    xml.startElement("memberships", {})

    renderer = XMLRenderer()
    for m in members:
        renderer.render_member(xml, m)

    xml.endElement("memberships")
    xml.endElement("root")
    xml.endDocument()

    frag_root = ET.fromstring(buf.getvalue())
    memberships_fragment = frag_root.find("memberships")

    # 2) load target project.xml and replace existing <memberships>
    tree = ET.parse(xml_path)
    root = tree.getroot()
    old = root.find("memberships")
    if old is not None:
        root.remove(old)
    root.append(memberships_fragment)

    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
