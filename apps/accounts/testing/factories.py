import factory

from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from ..models import *


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory('apps.accounts.testing.factories.UserFactory', profile=None)


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = 'user'
    password = 'user'

    first_name = 'Ulf'
    last_name = 'User'

    email = 'user@example.com'

    profile = factory.RelatedFactory(ProfileFactory, 'user')

    @classmethod
    def _generate(cls, create, attrs):
        post_save.disconnect(create_profile_for_user, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_profile_for_user, User)
        return user

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


class DetailKeyFactory(DjangoModelFactory):

    class Meta:
        model = DetailKey


class TextDetailKeyFactory(DetailKeyFactory):

    type = 'text'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'text'
    key = 'text'
    required = True


class TextareaDetailKeyFactory(DetailKeyFactory):

    type = 'textarea'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'textarea'
    key = 'textarea'
    required = True


class SelectDetailKeyFactory(DetailKeyFactory):

    type = 'select'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'select'
    key = 'select'
    required = True


class RadioDetailKeyFactory(DetailKeyFactory):

    type = 'radio'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'radio'
    key = 'radio'
    required = True


class MultiselectDetailKeyFactory(DetailKeyFactory):

    type = 'multiselect'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'multiselect'
    key = 'multiselect'
    required = True


class ChecboxDetailKeyFactory(DetailKeyFactory):

    type = 'checkbox'
    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
    label = 'checkbox'
    key = 'checkbox'
    required = True
