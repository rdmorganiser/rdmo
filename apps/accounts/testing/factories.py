from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from ..models import *


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = 'user'
    password = 'user'

    first_name = 'Ulf'
    last_name = 'User'

    email = 'user@example.com'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class ManagerFactory(UserFactory):

    username = 'manager'
    password = 'manager'

    first_name = 'Manni'
    last_name = 'Manager'

    email = 'manager@example.com'


class AdminFactory(UserFactory):

    username = 'admin'
    password = 'admin'

    first_name = 'Albert'
    last_name = 'Admin'

    email = 'admin@example.com'

    is_staff = True
    is_superuser = True


class AdditionalFieldFactory(DjangoModelFactory):

    class Meta:
        model = AdditionalField


class AdditionalTextFieldFactory(AdditionalFieldFactory):

    type = 'text'
    help_en = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    help_de = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    text_en = 'text'
    text_de = 'text'
    key = 'text'
    required = True


class AdditionalTextareaFieldFactory(AdditionalFieldFactory):

    type = 'textarea'
    help_en = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    help_de = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    text_en = 'textarea'
    text_de = 'textarea'
    key = 'textarea'
    required = True
