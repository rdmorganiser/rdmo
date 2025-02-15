import json
import logging
import os
import re
from pathlib import Path
from tempfile import mkstemp

from django.apps import apps
from django.conf import settings

import pypandoc
from packaging.version import Version
from packaging.version import parse as parse_version

log = logging.getLogger(__name__)


def get_pandoc_version():
    return parse_version(pypandoc.get_pandoc_version())


def get_pandoc_content(html, metadata, export_format, context):
    pandoc_args = get_pandoc_args(export_format, context)

    if metadata:
        # create a temporary file for the metadata
        (metadata_tmp_fd, metadata_tmp_file_name) = mkstemp(suffix='.json')

        # save metadata
        log.info('Save metadata file %s %s', metadata_tmp_file_name, str(metadata))
        with open(metadata_tmp_file_name, 'w') as fp:
            json.dump(metadata, fp)

        # add metadata file to pandoc args
        pandoc_args.append('--metadata-file=' + metadata_tmp_file_name)

    # create a temporary file
    (tmp_fd, tmp_file_name) = mkstemp(f'.{export_format}')

    # convert the file using pandoc
    log.info('Export %s document using args %s.', export_format, pandoc_args)
    html = re.sub(
        r'(<img.+src=["\'])' + settings.STATIC_URL + r'([\w\-\@?^=%&/~\+#]+)', r'\g<1>' +
        str(Path(settings.STATIC_ROOT)) + r'/\g<2>', html
    )
    pypandoc.convert_text(html, export_format, format='html', outputfile=tmp_file_name, extra_args=pandoc_args)

    # read the created temporary file
    with open(tmp_file_name, 'rb') as fp:
        pandoc_content = fp.read()

    # delete temporary files
    if metadata:
        os.remove(metadata_tmp_file_name)
    os.remove(tmp_file_name)

    return pandoc_content


def get_pandoc_content_disposition(export_format, title):
    if export_format == 'pdf':
        # display pdf in browser
        return f'filename="{title}.{export_format}"'
    else:
        return f'attachment; filename="{title}.{export_format}"'


def get_pandoc_args(export_format, context):
    view = context.get('view')
    pandoc_version = get_pandoc_version()
    pandoc_args = settings.EXPORT_PANDOC_ARGS.get(export_format, [])

    if export_format == 'pdf':
        # we used xelatex before pandoc 3
        if pandoc_version < Version('3'):
            pandoc_args = [
                arg.replace('--pdf-engine=lualatex', '--pdf-engine=xelatex')
                for arg in pandoc_args
            ]

    elif export_format in ['docx', 'odt']:
        # find and add a possible reference document
        reference_document = get_pandoc_reference_document(export_format, view)
        if reference_document:
            if pandoc_version >= Version('2'):
                pandoc_args.append(f'--reference-doc={reference_document}')
            else:
                pandoc_args.append(f'--reference-{export_format}={reference_document}')

    # add STATIC_ROOT and possible additional resource paths
    if pandoc_version >= Version('2'):
        pandoc_args.append(f'--resource-path={settings.STATIC_ROOT}')
        if 'resource_path' in context:
            resource_path = Path(settings.MEDIA_ROOT) / context['resource_path']
            pandoc_args.append(f'--resource-path={resource_path}')

    return pandoc_args


def get_pandoc_reference_document(export_format, view):
    # collect all configured reference documents
    reference_documents = get_pandoc_reference_documents(export_format, view)

    # return the first reference document that actually exists
    for reference_document in reference_documents:
        if reference_document and reference_document.exists():
            return Path(reference_document)


def get_pandoc_reference_documents(export_format, view):
    reference_documents = []

    if export_format == 'odt':
        # append view specific custom reference document
        if view is not None:
            reference_documents.append(settings.EXPORT_REFERENCE_ODT_VIEWS.get(view.uri))

        # append generic custom reference document
        if settings.EXPORT_REFERENCE_ODT:
            reference_documents.append(settings.EXPORT_REFERENCE_ODT)

        # append the default reference document
        reference_documents.append(Path(apps.get_app_config('rdmo').path) / 'share' / 'reference.odt')

    elif export_format == 'docx':
        # append view specific custom reference document
        if view is not None:
            reference_documents.append(settings.EXPORT_REFERENCE_DOCX_VIEWS.get(view.uri))

        # append generic custom reference document
        if settings.EXPORT_REFERENCE_DOCX:
            reference_documents.append(settings.EXPORT_REFERENCE_DOCX)

        # append the default reference document
        reference_documents.append(Path(apps.get_app_config('rdmo').path) / 'share' / 'reference.docx')

    return reference_documents
