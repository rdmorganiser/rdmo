import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.utils.six import StringIO

from test_generator.core import TestMixin

from rdmo.core.testing.utils import get_client, sanitize_xml, read_xml_file, fuzzy_compare


class TestExportViewMixin(TestMixin):

    export_formats = ('xml', 'html', 'rtf')

    def _test_export_list(self, username):

        for format in self.export_formats:
            url = reverse(self.url_names['export_view'], kwargs={'format': format})
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, self.status_map['export_view'][username])
            except AssertionError:
                print(
                    ('test', 'test_export'),
                    ('username', username),
                    ('url', url),
                    ('format', format),
                    ('status_code', response.status_code),
                    ('content', response.content)
                )
                raise


class TestImportViewMixin(TestMixin):

    import_formats = ('xml', )

    def _test_import_get(self, username):

        for format in self.import_formats:
            url = reverse(self.url_names['import_view'], kwargs={'format': format})
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, self.status_map['import_view'][username])

                if response.status_code == 302:
                    if username == 'anonymous':
                        self.assertRedirects(response, reverse('account_login') + '?next=' + url)
                    else:
                        self.assertRedirects(response, reverse(self.url_names['list_view']))

            except AssertionError:
                print(
                    ('test', 'test_import'),
                    ('username', username),
                    ('url', url),
                    ('status_code', response.status_code),
                    ('content', response.content)
                )
                raise

    def _test_import_post(self, username):

        for format in self.import_formats:

            url = reverse(self.url_names['import_view'], kwargs={'format': format})

            with open(self.import_file) as f:
                response = self.client.post(url, {'attachment': f})

            try:
                self.assertEqual(response.status_code, self.status_map['import_view'][username])
            except AssertionError:
                print(
                    ('test', 'test_import'),
                    ('username', username),
                    ('url', url),
                    ('status_code', response.status_code),
                    ('content', response.content)
                )
                raise


class TestImportManageMixin(TestMixin):

    def test_import(self):
        print('\n\nImporting file ' + self.import_file)
        logfile = settings.LOGGING_DIR + 'rdmo.log'
        out, err = StringIO(), StringIO()

        if os.path.isfile(logfile):
            open(logfile, 'w').close()

        try:
            call_command('import', self.import_file, '--user=%s' % self.import_user, stdout=out, stderr=err)
        except AttributeError:
            call_command('import', self.import_file, stdout=out, stderr=err)

        # assert exitcode and possible error message
        self.assertFalse(out.getvalue())
        self.assertFalse(err.getvalue())

        # assert logfile
        if os.path.isfile(logfile):
            self.assert_log(logfile)

        if self.compare_import_to_export_data is True:
            successful = self.assert_export_data()
            if successful is True:
                print('Import export compare was successful.')
            else:
                print('Import export compare failed.')

    def assert_log(self, logfile):
        successful = True
        with open(logfile, 'r') as fh:
            lines = fh.read().splitlines()
        for l in lines:
            if '[ERROR]' in l:
                print('\n' + l)
                successful = False
        if successful is False:
            self.assertFalse('Found error messages in logfile.')

    def assert_export_data(self):
        client = get_client()
        response = client.get(reverse(self.export_api, kwargs=self.export_api_kwargs))
        exported_xml_data = sanitize_xml(response.content)
        imported_xml_data = read_xml_file(self.import_file)

        successful = fuzzy_compare(imported_xml_data, exported_xml_data, self.compare_import_to_export_ignore_list)
        if successful is False:
            self.assertFalse('Export data differ from import data')
        return successful
