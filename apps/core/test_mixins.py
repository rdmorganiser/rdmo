import json

from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict


class TestSingleObjectMixin(object):

    def model_to_dict(self, instance=None):
        if instance is None:
            instance = self.instance

        model_dict = model_to_dict(instance)
        model_data = {}
        for key in model_dict:
            if model_dict[key] is not None:
                model_data[key] = model_dict[key]

        return model_data


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
        response = self.client.post(url, self.model_to_dict())
        self.assertEqual(response.status_code, 302)


class TestUpdateViewMixin(TestSingleObjectMixin):

    def test_update_view_get(self):
        url = reverse(self.update_url_name, args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_post(self):
        url = reverse(self.update_url_name, args=[self.instance.pk])
        response = self.client.post(url, self.model_to_dict())
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


class TestModelStringMixin(TestSingleObjectMixin):

    def test_model_str(self):
        self.assertIsNotNone(self.instance.__str__())


class TestListAPIViewMixin(object):

    def test_list_api_view(self):
        url = reverse(self.api_url_name + '-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRetrieveAPIViewMixin(object):

    def test_retrieve_api_view(self):
        url = reverse(self.api_url_name + '-detail', args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateAPIViewMixin(TestSingleObjectMixin):

    def test_create_api_view(self):
        url = reverse(self.api_url_name + '-list')
        response = self.client.post(url, self.model_to_dict())
        self.assertEqual(response.status_code, 201)


class TestUpdateAPIViewMixin(TestSingleObjectMixin):

    def test_update_api_view(self):
        url = reverse(self.api_url_name + '-detail', args=[self.instance.pk])
        data = json.dumps(self.model_to_dict())
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class TestDeleteAPIViewMixin(TestSingleObjectMixin):

    def test_delete_api_view(self):
        url = reverse(self.api_url_name + '-detail', args=[self.instance.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class TestModelAPIViewMixin(TestListAPIViewMixin,
                            TestRetrieveAPIViewMixin,
                            TestCreateAPIViewMixin,
                            TestUpdateAPIViewMixin,
                            TestDeleteAPIViewMixin):
    pass
