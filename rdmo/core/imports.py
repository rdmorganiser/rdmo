import logging
import time
import defusedxml.ElementTree as ET
from random import randint

log = logging.getLogger(__name__)


def get_value_from_xml_node(xml_node, element, what_to_get=None):
    r = ''
    try:
        if what_to_get == 'attrib':
            r = xml_node.find(element).attrib
        elif what_to_get == 'tag':
            r = xml_node.find(element).tag
        else:
            r = xml_node.find(element).text
    except Exception as e:
        log.debug('Unable to extract "' + element + '" from "' + str(xml_node) + '". ' + str(e))
        pass
    else:
        if r is None:
            r = ''
        try:
            r = r.encode('utf-8', 'ignore')
        except Exception as e:
            log.debug('Unable to decode string to utf-8: ' + str(e))
            pass
    return r


def generate_tempfile_name():
    t = int(round(time.time() * 1000))
    r = randint(10000, 99999)
    fn = '/tmp/upload_' + str(t) + '_' + str(r) + '.xml'
    return fn


def handle_uploaded_file(filedata):
    tempfilename = generate_tempfile_name()
    with open(tempfilename, 'wb+') as destination:
        for chunk in filedata.chunks():
            destination.write(chunk)
    return tempfilename


def validate_xml(tempfilename, root_tag):
    tree = None
    exit_code = 0
    try:
        tree = ET.parse(tempfilename)
    except Exception as e:
        exit_code = 1
        log.info('Xml parsing error: ' + str(e))
        pass
    else:
        root = tree.getroot()
        if root.tag != root_tag:
            log.info('Validation failed. Xml\'s root node is "' + root.tag + '" and not "' + root_tag + '".')
            exit_code = 1
    return exit_code, tree
