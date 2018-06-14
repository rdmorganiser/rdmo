import xml.dom.minidom


def prettify_xml(xmlstring):
    xmlobj = xml.dom.minidom.parseString(xmlstring)
    return xmlobj.toprettyxml()
