from django.core.urlresolvers import reverse
from django.core.management import call_command

from django.utils import translation
from django.utils.six import StringIO


class TestExportViewMixin(object):

    export_formats = ('xml', 'html', 'rtf')

    def test_export_list(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

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

            self.client.logout()


class TestImportViewMixin(object):

    def test_import(self):
        out, err = StringIO(), StringIO()

        call_command('import', self.import_file, stdout=out, stderr=err)
        self.assertFalse(out.getvalue())
        self.assertFalse(err.getvalue())
