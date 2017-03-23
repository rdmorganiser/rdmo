import json

from datetime import datetime, timedelta
from itertools import chain

from django.core.urlresolvers import reverse
from django.core.management import call_command

from django.utils import translation
from django.utils.six import StringIO


class TestSingleObjectMixin(object):

    def model_to_dict(self, instance):
        # the folowing is taken from the 1.9 version of django.forms.models.model_to_dict
        from django.db.models.fields.related import ManyToManyField
        opts = instance._meta
        data = {}
        for field in chain(opts.concrete_fields, opts.virtual_fields, opts.many_to_many):
            if not getattr(field, 'editable', False):
                continue
            if isinstance(field, ManyToManyField):
                # If the object doesn't have a primary key yet, just use an empty
                # list for its m2m fields. Calling f.value_from_object will raise
                # an exception.
                if instance.pk is None:
                    data[field.name] = []
                else:
                    # MultipleChoiceWidget needs a list of pks, not object instances.
                    qs = field.value_from_object(instance)
                    if qs._result_cache is not None:
                        data[field.name] = [item.pk for item in qs]
                    else:
                        data[field.name] = list(qs.values_list('pk', flat=True))
            else:
                data[field.name] = field.value_from_object(instance)

        return data

    def get_instance_as_dict(self, instance=None):
        if instance is None:
            instance = self.instance

        model_dict = self.model_to_dict(instance)

        model_data = {}
        for key in model_dict:
            model_value = model_dict[key]

            if model_value is not None:
                if isinstance(model_value, datetime):
                    model_data[key] = model_value.isoformat()
                elif isinstance(model_value, timedelta):
                    model_data[key] = str(model_value)
                else:
                    model_data[key] = model_value

        return model_data

    def get_instance_as_json(self, instance=None):
        return json.dumps(self.get_instance_as_dict(instance))


class TestListViewMixin(object):

    def test_list_view(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            url = reverse(self.url_names['list'], args=self.get_list_url_args())
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, self.status_map['list'][username])
            except AssertionError:
                print(
                    ('test', 'test_list_view'),
                    ('username', username),
                    ('url', url),
                    ('status_code', response.status_code),
                    ('content', response.content)
                )
                raise

            self.client.logout()

    def get_list_url_args(self):
        return []


class TestRetrieveViewMixin(object):

    def test_retrieve_view(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                url = reverse(self.url_names['retrieve'], args=self.get_retrieve_url_args(instance))
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['retrieve'][username])
                except AssertionError:
                    print(
                        ('test', 'test_retrieve_view'),
                        ('username', username),
                        ('url', url),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def get_retrieve_url_args(self, instance):
        return [instance.pk]


class TestCreateViewMixin(TestSingleObjectMixin):

    def test_create_view_get(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            url = reverse(self.url_names['create'], args=self.get_create_url_args())
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, self.status_map['create']['get'][username])
            except AssertionError:
                print(
                    ('test', 'test_create_view_get'),
                    ('username', username),
                    ('url', url),
                    ('status_code', response.status_code),
                    ('content', response.content)
                )
                raise

            self.client.logout()

    def test_create_view_post(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_create_instance(instance)

                url = reverse(self.url_names['create'], args=self.get_create_url_args())
                data = self.get_instance_as_dict(instance)
                response = self.client.post(url, data)

                try:
                    self.assertEqual(response.status_code, self.status_map['create']['post'][username])
                except AssertionError:
                    print(
                        ('test', 'test_create_view_post'),
                        ('username', username),
                        ('url', url),
                        ('data', data),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def get_create_url_args(self):
        return []

    def prepare_create_instance(self, instance):
        return instance


class TestUpdateViewMixin(TestSingleObjectMixin):

    def test_update_view_get(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_update_instance(instance)

                url = reverse(self.url_names['update'], args=self.get_update_url_args(instance))
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['update']['get'][username])
                except AssertionError:
                    print(
                        ('test', 'test_update_view_get'),
                        ('username', username),
                        ('url', url),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def test_update_view_post(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_update_instance(instance)

                url = reverse(self.url_names['update'], args=self.get_update_url_args(instance))
                data = self.get_instance_as_dict(instance)
                response = self.client.post(url, data)

                try:
                    self.assertEqual(response.status_code, self.status_map['update']['post'][username])
                except AssertionError:
                    print(
                        ('test', 'test_update_view_post'),
                        ('username', username),
                        ('url', url),
                        ('data', data),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def get_update_url_args(self, instance):
        return [instance.pk]

    def prepare_update_instance(self, instance):
        return instance


class TestDeleteViewMixin(TestSingleObjectMixin):

    def test_delete_view_get(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_update_instance(instance)

                url = reverse(self.url_names['delete'], args=self.get_delete_url_args(instance))
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['delete']['get'][username])
                except AssertionError:
                    print(
                        ('test', 'test_delete_view_get'),
                        ('username', username),
                        ('url', url),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def test_delete_view_post(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_delete_instance(instance)

                url = reverse(self.url_names['delete'], args=self.get_delete_url_args(instance))
                response = self.client.post(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['delete']['post'][username])

                    # save the instance again so we can delete it again later
                    instance.save()
                except AssertionError:
                    print(
                        ('test', 'test_update_view_post'),
                        ('username', username),
                        ('url', url),
                        ('status_code', response.status_code),
                        ('content', response.content)
                    )
                    raise

            self.client.logout()

    def get_delete_url_args(self, instance):
        return [instance.pk]

    def prepare_delete_instance(self, instance):
        return instance


class TestModelViewMixin(TestListViewMixin,
                         TestRetrieveViewMixin,
                         TestCreateViewMixin,
                         TestUpdateViewMixin,
                         TestDeleteViewMixin):
    pass


class TestModelStringMixin(TestSingleObjectMixin):

    def test_model_str(self):
        for instance in self.instances:
            self.assertIsNotNone(instance.__str__())


class TestExportViewMixin(object):

    export_formats = ('xml', 'html', 'rtf')

    def test_export_list(self):
        translation.activate(self.lang)

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for format in self.export_formats:
                url = reverse(self.url_names['export'], kwargs={'format': format})
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.status_map['export'][username])
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


class TestListAPIViewMixin(object):

    def test_list_api_view(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            url = reverse(self.api_url_name + '-list')
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, self.api_status_map['list'][username])
            except AssertionError:
                print(
                    ('test', 'test_list_api_view'),
                    ('username', username),
                    ('url',  url),
                    ('status_code',  response.status_code),
                    ('json',  response.json())
                )
                raise


class TestRetrieveAPIViewMixin(object):

    def test_retrieve_api_view(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_retrieve_instance(instance)

                url = reverse(self.api_url_name + '-detail', args=[instance.pk])
                response = self.client.get(url)

                try:
                    self.assertEqual(response.status_code, self.api_status_map['retrieve'][username])
                except AssertionError:
                    print(
                        ('test', 'test_retrieve_api_view'),
                        ('username', username),
                        ('url',  url),
                        ('status_code',  response.status_code),
                        ('json',  response.json())
                    )
                    raise

    def prepare_retrieve_instance(self, instance):
        return instance


class TestCreateAPIViewMixin(TestSingleObjectMixin):

    def test_create_api_view(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_create_instance(instance)

                url = reverse(self.api_url_name + '-list')
                data = self.get_instance_as_dict(instance)
                response = self.client.post(url, self.get_instance_as_dict(instance))

                try:
                    self.assertEqual(response.status_code, self.api_status_map['create'][username])
                except AssertionError:
                    print(
                        ('test', 'test_create_api_view'),
                        ('username', username),
                        ('url',  url),
                        ('data',  data),
                        ('status_code',  response.status_code),
                        ('json',  response.json())
                    )
                    raise

    def prepare_create_instance(self, instance):
        return instance


class TestUpdateAPIViewMixin(TestSingleObjectMixin):

    def test_update_api_view(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_update_instance(instance)

                url = reverse(self.api_url_name + '-detail', args=[instance.pk])
                data = self.get_instance_as_json(instance)
                response = self.client.put(url, data, content_type="application/json")

                try:
                    self.assertEqual(response.status_code, self.api_status_map['update'][username])
                except AssertionError:
                    print(
                        ('test', 'test_update_api_view'),
                        ('username', username),
                        ('url',  url),
                        ('data',  data),
                        ('status_code',  response.status_code),
                        ('json',  response.json())
                    )
                    raise

    def prepare_update_instance(self, instance):
        return instance


class TestDeleteAPIViewMixin(TestSingleObjectMixin):

    def test_delete_api_view(self):

        for username, password in self.users:
            if password:
                self.client.login(username=username, password=password)

            for instance in self.instances:
                instance = self.prepare_delete_instance(instance)

                url = reverse(self.api_url_name + '-detail', args=[instance.pk])
                response = self.client.delete(url)
                try:
                    self.assertEqual(response.status_code, self.api_status_map['delete'][username])
                except AssertionError:
                    print(
                        ('test', 'test_delete_api_view'),
                        ('username', username),
                        ('url',  url),
                        ('status_code',  response.status_code),
                        ('json',  response.json())
                    )
                    raise

    def prepare_delete_instance(self, instance):
        return instance


class TestModelAPIViewMixin(TestListAPIViewMixin,
                            TestRetrieveAPIViewMixin,
                            TestCreateAPIViewMixin,
                            TestUpdateAPIViewMixin,
                            TestDeleteAPIViewMixin):
    pass
