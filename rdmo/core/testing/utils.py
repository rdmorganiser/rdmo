# import logging
# import re

# from django.test import Client
# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist

# logger = logging.getLogger(__name__)


# def get_super_client():
#     try:
#         User.objects.get(username='admin')
#     except ObjectDoesNotExist:
#         user = User.objects.create_superuser('admin', 'admin@test.rdmo', 'admin')
#         user.save()
#     client = Client()
#     client.login(username='admin', password='admin')
#     return client


# def sanitize_xml(xmldata):
#     xmldata = xmldata.decode('utf-8')
#     xmldata = re.sub('(\n|\t)', '', xmldata)
#     return xmldata


# def read_xml_file(filename):
#     with open(filename, 'r', encoding='utf-8') as filedata:
#         xmlstring = ''
#         for line in filedata:
#             ll = line.rstrip().lstrip()
#             xmlstring += ll
#     return xmlstring


# def fuzzy_compare(imported_data, exported_data, ignore_list):
#     successful = True
#     imported_data_compare = get_elements_to_compare(imported_data, ignore_list)
#     exported_data_compare = get_elements_to_compare(exported_data, ignore_list)
#     for el in imported_data_compare:
#         if el not in exported_data_compare:
#             logger.debug('Element "%s" from import data is not in exported dataset', el)
#             successful = False
#     # for el in exported_data_compare:
#     #     if el not in imported_data_compare:
#     #         print('\nElement "' + el + '" from exported dataset is not in import data')
#     #         successful = False
#     return successful


# def get_elements_to_compare(xmldata, ignore_list):
#     findings = []
#     arr = re.findall('[A-Za-z0-9_:-]+\>.*?(?=\<)', xmldata)
#     for s in arr:
#         if s.endswith('>') is False and is_in_ignore_list(s, ignore_list) is False:
#             try:
#                 s = s.encode('utf-8')
#             except Exception as e:
#                 logger.debug(e)
#                 pass
#             findings.append(s)
#     return sorted(remove_duplicates(findings))


# def is_in_ignore_list(s, ignore_list):
#     is_in_list = False
#     s = s.split('>')[0]
#     for el in ignore_list:
#         if el.startswith(s) is True:
#             is_in_list = True
#             break
#     return is_in_list


# def remove_duplicates(l):
#     return list(set(l))
