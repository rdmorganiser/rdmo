import hashlib
import re

from django.test import Client


def get_client():
    client = Client()
    client.login(username='admin', password='admin')
    return client


def sanitize_xml(xmldata):
    xmldata = xmldata.decode('utf-8')
    xmldata = re.sub('(\n|\t)', '', xmldata)
    return xmldata


def read_xml_file(filename):
    with open(filename, 'r') as filedata:
        xmlstring = ''
        for line in filedata:
            ll = line.rstrip().lstrip()
            xmlstring += ll
    return xmlstring


def get_elements_to_compare(xmldata):
    findings = []
    arr = re.findall('[A-Za-z0-9_:-]+\>.*?(?=\<)', xmldata)
    for s in arr:
        if s.endswith('>') is False:
            findings.append(s)
    return findings


def fuzzy_compare(xmldata1, xmldata2):
    success = True
    compare_set1 = get_elements_to_compare(xmldata1)
    compare_set2 = get_elements_to_compare(xmldata2)
    for e1 in compare_set1:
        if e1 in compare_set2 is False:
            print('Element "' + e1 + '" from dataset 1 is not in dataset 2')
            success = False
    for e2 in compare_set2:
        if e2 in compare_set1 is False:
            print('Element "' + e2 + '" from dataset 2 is not in dataset 1')
            success = False
    return success
