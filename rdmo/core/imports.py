import logging
import time
from random import randint

import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


# def make_bool(instring):
#     r = None
#     s = instring
#     try:
#         s = s.decode('utf-8')
#     except AttributeError:
#         pass
#     truelist = ['True', 'true']
#     falselist = ['False', 'false']
#     if s in truelist:
#         r = True
#     elif s in falselist:
#         r = False
#     return r


# def get_value_from_treenode(xml_node, element, what_to_get=None):
#     r = ''
#     try:
#         if what_to_get == 'attrib':
#             r = xml_node.find(element).attrib
#         elif what_to_get == 'tag':
#             r = xml_node.find(element).tag
#         else:
#             r = xml_node.find(element).text
#     except Exception as e:
#         log.debug('Unable to extract "' + element + '" from "' + str(xml_node) + '". ' + str(e))
#         pass
#     else:
#         if r is None:
#             r = ''
#         try:
#             r = r.encode('utf-8', 'ignore')
#         except Exception as e:
#             log.debug('Unable to decode string to utf-8: ' + str(e))
#             pass
#     return r


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


def open_uploaded_file(tempfilename):
    tempfilename = generate_tempfile_name()
    return open(tempfilename)


# TODO should be moved to xml.py
def read_xml_file(filename):
    tree = None
    try:
        tree = ET.parse(filename).getroot()
    except Exception as e:
        log.error('Xml parsing error: ' + str(e))
    return tree


def set_lang_field(instance, field_name, element, lang_code, lang_field):
    field = element.get('%s_%s' % (field_name, lang_code))
    if field:
        setattr(instance, '%s_%s' % (field_name, lang_field), field)
