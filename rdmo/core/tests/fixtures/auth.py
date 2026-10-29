import pytest

from django.contrib.auth.models import User


@pytest.fixture
def login(client):
    def force_login_user(username):
        try:
            user = User.objects.get(username=username)
            client.force_login(user)
        except User.DoesNotExist:
            pass

    return force_login_user
