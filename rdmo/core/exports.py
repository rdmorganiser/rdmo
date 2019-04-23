from xml.dom.minidom import parseString


def prettify_xml(xmlstring):
    xmlobj = parseString(xmlstring)
    return xmlobj.toprettyxml()
