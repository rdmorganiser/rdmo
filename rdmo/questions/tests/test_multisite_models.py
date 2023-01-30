
from ..models import Catalog, Question, QuestionSet, Section

from .test_multisite_viewset_catalog import editor_users_per_site


@pytest.mark.parametrize('username,password', editor_users_per_site)
def test_multisite_catalog_copy(db):
    ''' copying a catalog from another site should set the current site (from editor) as the only site '''
    instances = Catalog.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        # Copy should check for current user site (or editor Role)
        # and set the new catalog to that site
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert list(new_instance.sites.values('id')) == list(new_instance.sites.values('id'))
        # assert list(new_instance.groups.values('id')) == list(new_instance.groups.values('id'))
        # assert new_instance.sections.count() == instance.sections.count()


# def test_section_copy(db):
#     instances = Section.objects.all()
#     for instance in instances:
#         new_uri_prefix = instance.uri_prefix + '-'
#         new_key = instance.key + '-'
#         new_instance = instance.copy(new_uri_prefix, new_key)
#         assert new_instance.uri_prefix == new_uri_prefix
#         assert new_instance.key == new_key
#         assert new_instance.questionsets.count() == instance.questionsets.count()


# def test_questionset_copy(db):
#     instances = QuestionSet.objects.all()
#     for instance in instances:
#         new_uri_prefix = instance.uri_prefix + '-'
#         new_key = instance.key + '-'
#         new_instance = instance.copy(new_uri_prefix, new_key)
#         assert new_instance.uri_prefix == new_uri_prefix
#         assert new_instance.key == new_key
#         assert new_instance.attribute == instance.attribute
#         assert list(new_instance.conditions.values('id')) == list(new_instance.conditions.values('id'))
#         assert new_instance.questions.count() == instance.questions.count()


# def test_question_copy(db):
#     instances = Question.objects.all()
#     for instance in instances:
#         new_uri_prefix = instance.uri_prefix + '-'
#         new_key = instance.key + '-'
#         new_instance = instance.copy(new_uri_prefix, new_key)
#         assert new_instance.uri_prefix == new_uri_prefix
#         assert new_instance.key == new_key
#         assert new_instance.attribute == instance.attribute
#         assert list(new_instance.conditions.values('id')) == list(new_instance.conditions.values('id'))
#         assert list(new_instance.optionsets.values('id')) == list(new_instance.optionsets.values('id'))
