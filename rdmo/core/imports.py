import logging
import tempfile
import time
from os.path import join as pj
from random import randint

import defusedxml.ElementTree as ET

log = logging.getLogger(__name__)


def generate_tempfile_name():
    t = int(round(time.time() * 1000))
    r = randint(10000, 99999)
    fn = pj(tempfile.gettempdir(), 'upload_' + str(t) + '_' + str(r) + '.xml')
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
