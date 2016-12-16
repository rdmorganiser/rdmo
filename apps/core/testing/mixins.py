from datetime import datetime, timedelta
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class TestSingleObjectMixin(object):

    def get_instance_as_dict(self, instance=None):
        if instance is None:
            instance = self.instance

        model_dict = model_to_dict(instance)

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
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRetrieveViewMixin(object):

    def test_retrieve_view(self):
        url = reverse(self.retrieve_url_name, args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateViewMixin(TestSingleObjectMixin):

    def test_create_view_get(self):
        url = reverse(self.create_url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_post(self):
        url = reverse(self.create_url_name)
        response = self.client.post(url, self.get_instance_as_dict())
        self.assertEqual(response.status_code, 302)


class TestUpdateViewMixin(TestSingleObjectMixin):

    def test_update_view_get(self):
        url = reverse(self.update_url_name, args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_post(self):
        url = reverse(self.update_url_name, args=[self.instance.pk])
        response = self.client.post(url, self.get_instance_as_dict())
        self.assertEqual(response.status_code, 302)


class TestDeleteViewMixin(TestSingleObjectMixin):

    def test_delete_view_get(self):
        url = reverse(self.delete_url_name, args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_post(self):
        url = reverse(self.delete_url_name, args=[self.instance.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class TestModelViewMixin(TestListViewMixin,
                         TestRetrieveViewMixin,
                         TestCreateViewMixin,
                         TestUpdateViewMixin,
                         TestDeleteViewMixin):
    pass


class TestModelStringMixin(TestSingleObjectMixin):

    def test_model_str(self):
        self.assertIsNotNone(self.instance.__str__())


class TestListAPIViewMixin(object):

    def test_list_api_view(self):
        url = reverse(self.api_url_name + '-list')
        response = self.client.get(url)

        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            print({
                'test': 'test_list_api_view',
                'url': url,
                'status_code': response.status_code,
                'json': response.json()
            })
            raise


class TestRetrieveAPIViewMixin(object):

    def test_retrieve_api_view(self):

        for instance in self.instances:
            instance = self.prepare_retrieve_instance(instance)

            url = reverse(self.api_url_name + '-detail', args=[instance.pk])
            response = self.client.get(url)

            try:
                self.assertEqual(response.status_code, 200)
            except AssertionError:
                print(
                    ('test', 'test_retrieve_api_view'),
                    ('url',  url),
                    ('status_code',  response.status_code),
                    ('response',  response.json())
                )
                raise

    def prepare_retrieve_instance(self, instance):
        return instance


class TestCreateAPIViewMixin(TestSingleObjectMixin):

    def test_create_api_view(self):

        for instance in self.instances:
            instance = self.prepare_create_instance(instance)

            url = reverse(self.api_url_name + '-list')
            data = self.get_instance_as_dict(instance)
            response = self.client.post(url, self.get_instance_as_dict(instance))

            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(
                    ('test', 'test_create_api_view'),
                    ('url',  url),
                    ('data',  data),
                    ('status_code',  response.status_code),
                    ('response',  response.json())
                )
                raise

    def prepare_create_instance(self, instance):
        return instance


class TestUpdateAPIViewMixin(TestSingleObjectMixin):

    def test_update_api_view(self):

        for instance in self.instances:
            instance = self.prepare_update_instance(instance)

            url = reverse(self.api_url_name + '-detail', args=[instance.pk])
            data = self.get_instance_as_json(instance)
            response = self.client.put(url, data, content_type="application/json")

            try:
                self.assertEqual(response.status_code, 200)
            except AssertionError:
                print(
                    ('test', 'test_update_api_view'),
                    ('url',  url),
                    ('data',  data),
                    ('status_code',  response.status_code),
                    ('response',  response.json())
                )
                raise

    def prepare_update_instance(self, instance):
        return instance


class TestDeleteAPIViewMixin(TestSingleObjectMixin):

    def test_delete_api_view(self):

        for instance in self.instances:
            instance = self.prepare_delete_instance(instance)

            url = reverse(self.api_url_name + '-detail', args=[instance.pk])
            response = self.client.delete(url)
            try:
                self.assertEqual(response.status_code, 204)
            except AssertionError:
                print(
                    ('test', 'test_delete_api_view'),
                    ('url',  url),
                    ('status_code',  response.status_code),
                    ('response',  response.json())
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
