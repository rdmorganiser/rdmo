import logging
import time
import defusedxml.ElementTree as ET
from random import randint

log = logging.getLogger(__name__)


def make_bool(instring):
    r = None
    s = instring
    try:
        s = s.decode('utf-8')
    except AttributeError:
        pass
    truelist = ['True', 'true']
    falselist = ['False', 'false']
    if s in truelist:
        r = True
    elif s in falselist:
        r = False
    return r


def get_value_from_treenode(xml_node, element, what_to_get=None):
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


def validate_xml(tempfilename):
    tree = None
    roottag = None
    try:
        tree = ET.parse(tempfilename)
    except Exception as e:
        log.error('Xml parsing error: ' + str(e))
        pass
    else:
        root = tree.getroot()
        roottag = root.tag
    return roottag, tree
