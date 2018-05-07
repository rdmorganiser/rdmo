from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.utils.six import StringIO

from test_generator.core import TestMixin


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
        out, err = StringIO(), StringIO()

        try:
            call_command('import', self.import_file, '--user=%s' % self.import_user, stdout=out, stderr=err)
        except AttributeError:
            call_command('import', self.import_file, stdout=out, stderr=err)

        self.assertFalse(out.getvalue())
        self.assertFalse(err.getvalue())
