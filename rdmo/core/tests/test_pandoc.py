from pathlib import Path

import pytest

from django.apps import apps

from packaging.version import Version

from ..pandoc import (
    get_pandoc_args,
    get_pandoc_content,
    get_pandoc_content_disposition,
    get_pandoc_reference_document,
    get_pandoc_reference_documents,
    get_pandoc_version,
)

rdmo_path = Path(apps.get_app_config('rdmo').path)
testing_path = rdmo_path.parent / 'testing'

pandoc_versions = [
    '1.9.0',
    '2.0.0',
    '3.0.0',
    '3.5.0'
]

export_formats = [
    'rtf',
    'odt',
    'docx',
    'html',
    'markdown',
    'tex',
    'pdf'
]

pandoc_args_map = {
    '1.9.0': {
        'pdf': ['-V', 'geometry:a4paper, margin=1in', '--pdf-engine=xelatex'],
        'rtf': ['--standalone'],
        'docx': [f'--reference-docx={rdmo_path}/share/reference.docx'],
        'odt': [f'--reference-odt={rdmo_path}/share/reference.odt'],
        'other': []
    },
    '2.0.0': {
        'pdf': ['-V', 'geometry:a4paper, margin=1in', '--pdf-engine=xelatex',
                f'--resource-path={testing_path}/static_root'],
        'rtf': ['--standalone', f'--resource-path={testing_path}/static_root'],
        'docx': [f'--reference-doc={rdmo_path}/share/reference.docx', f'--resource-path={testing_path}/static_root'],
        'odt': [f'--reference-doc={rdmo_path}/share/reference.odt', f'--resource-path={testing_path}/static_root'],
        'other': [f'--resource-path={testing_path}/static_root']
    },
    '3.0.0': {
        'pdf': ['-V', 'geometry:a4paper, margin=1in', '--pdf-engine=lualatex',
                f'--resource-path={testing_path}/static_root'],
        'rtf': ['--standalone', f'--resource-path={testing_path}/static_root'],
        'docx': [f'--reference-doc={rdmo_path}/share/reference.docx', f'--resource-path={testing_path}/static_root'],
        'odt': [f'--reference-doc={rdmo_path}/share/reference.odt', f'--resource-path={testing_path}/static_root'],
        'other': [f'--resource-path={testing_path}/static_root']
    },
    '3.5.0': {
        'pdf': ['-V', 'geometry:a4paper, margin=1in', '--pdf-engine=lualatex',
                f'--resource-path={testing_path}/static_root'],
        'rtf': ['--standalone', f'--resource-path={testing_path}/static_root'],
        'docx': [f'--reference-doc={rdmo_path}/share/reference.docx', f'--resource-path={testing_path}/static_root'],
        'odt': [f'--reference-doc={rdmo_path}/share/reference.odt', f'--resource-path={testing_path}/static_root'],
        'other': [f'--resource-path={testing_path}/static_root']
    }
}

class MockedView:
    uri = 'http://example.com/terms/views/view'


@pytest.mark.parametrize('pandoc_version', pandoc_versions)
def test_get_pandoc_version(mocker, pandoc_version):
    mocker.patch('pypandoc.get_pandoc_version', return_value=pandoc_version)
    assert get_pandoc_version() == Version(pandoc_version)


@pytest.mark.parametrize('pandoc_version', pandoc_versions)
@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_args(settings, mocker, pandoc_version, export_format):
    mocker.patch('pypandoc.get_pandoc_version', return_value=pandoc_version)
    pandoc_args = pandoc_args_map[pandoc_version].get(export_format, pandoc_args_map[pandoc_version]['other'])

    assert get_pandoc_args(export_format, {}) == pandoc_args


@pytest.mark.parametrize('pandoc_version', pandoc_versions)
@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_args_resource_path(settings, mocker, pandoc_version, export_format):
    mocker.patch('pypandoc.get_pandoc_version', return_value=pandoc_version)
    pandoc_args = pandoc_args_map[pandoc_version].get(export_format, pandoc_args_map[pandoc_version]['other']).copy()

    if Version(pandoc_version) >= Version('2'):
        pandoc_args.append('--resource-path=/Users/jochen/code/rdmorganiser/rdmo/testing/media_root/test')

    assert get_pandoc_args(export_format, {'resource_path': 'test'}) == pandoc_args


def test_get_pandoc_reference_document(mocker):
    mocker.patch('rdmo.core.pandoc.get_pandoc_reference_documents', return_value=[
        rdmo_path / 'share' / 'missing.docx',
        rdmo_path / 'share' / 'reference.docx',
        rdmo_path / 'share' / 'reference.odt'
    ])

    # return the first existing file
    assert get_pandoc_reference_document('other', {}) == rdmo_path / 'share' / 'reference.docx'


def test_get_pandoc_reference_document_missing(mocker):
    mocker.patch('rdmo.core.pandoc.get_pandoc_reference_documents', return_value=[
        rdmo_path / 'share' / 'missing.docx',
        rdmo_path / 'share' / 'missing.odt'
    ])

    assert get_pandoc_reference_document('other', {}) is None


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_reference_documents(export_format):
    rdmo_path = Path(apps.get_app_config('rdmo').path)

    reference_documents = get_pandoc_reference_documents(export_format, {})

    if export_format in ['docx', 'odt']:
        assert reference_documents == [rdmo_path / 'share' / f'reference.{export_format}']
    else:
        assert reference_documents == []


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_reference_documents_view(export_format):
    reference_documents = get_pandoc_reference_documents(export_format, {'view': MockedView()})

    if export_format in ['docx', 'odt']:
        assert reference_documents == [rdmo_path / 'share' / f'reference.{export_format}']
    else:
        assert reference_documents == []


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_reference_documents_view_settings(settings, export_format):
    mock_file = rdmo_path / 'share' / f'mock.{export_format}'

    if export_format == 'docx':
        settings.EXPORT_REFERENCE_DOCX_VIEWS = {'http://example.com/terms/views/view': mock_file}
    elif export_format == 'odt':
        settings.EXPORT_REFERENCE_ODT_VIEWS = {'http://example.com/terms/views/view': mock_file}

    reference_documents = get_pandoc_reference_documents(export_format, {'view': MockedView()})

    if export_format in ['docx', 'odt']:
        assert reference_documents == [mock_file, rdmo_path / 'share' / f'reference.{export_format}']
    else:
        assert reference_documents == []


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_reference_documents_settings(settings, export_format):
    mock_file = rdmo_path / 'share' / f'mock.{export_format}'

    if export_format == 'docx':
        settings.EXPORT_REFERENCE_DOCX = mock_file
    elif export_format == 'odt':
        settings.EXPORT_REFERENCE_ODT = mock_file

    reference_documents = get_pandoc_reference_documents(export_format, {})

    if export_format in ['docx', 'odt']:
        assert reference_documents == [mock_file, rdmo_path / 'share' / f'reference.{export_format}']
    else:
        assert reference_documents == []


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_content(settings, export_format):
    html_path = settings.BASE_DIR / 'export' / 'project.html'
    html = html_path.read_text()

    metadata = {
        'title': 'this is a very nice title',
        'author': ['author one', 'author two'],
        'keywords': ['nothing', 'something', 'whatever']
    }

    assert len(get_pandoc_content(html, metadata, export_format, {})) > 0


@pytest.mark.parametrize('export_format', export_formats)
def test_get_pandoc_content_disposition(export_format):
    title = 'Test'

    if export_format == 'pdf':
        content_disposition = f'filename="{title}.{export_format}"'
    else:
        content_disposition = f'attachment; filename="{title}.{export_format}"'

    assert get_pandoc_content_disposition(export_format, 'Test') == content_disposition
