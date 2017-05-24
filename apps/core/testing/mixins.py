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

    def test_import(self):
        out, err = StringIO(), StringIO()

        call_command('import', self.import_file, stdout=out, stderr=err)
        self.assertFalse(out.getvalue())
        self.assertFalse(err.getvalue())
