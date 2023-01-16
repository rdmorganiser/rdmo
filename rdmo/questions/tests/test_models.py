from ..models import Catalog, Page, Question, QuestionSet, Section


def test_catalog_str(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert str(instance)


def test_catalog_clean(db):
    instances = Catalog.objects.all()
    for instance in instances:
        instance.clean()


def test_catalog_copy(db):
    instances = Catalog.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_uri_path = instance.uri_path + '-'
        new_instance = instance.copy(new_uri_prefix, new_uri_path)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.uri_path == new_uri_path
        assert list(new_instance.sites.values('id')) == list(instance.sites.values('id'))
        assert list(new_instance.groups.values('id')) == list(instance.groups.values('id'))
        assert new_instance.sections.count() == instance.sections.count()


def test_section_str(db):
    instances = Section.objects.all()
    for instance in instances:
        assert str(instance)


def test_section_clean(db):
    instances = Section.objects.all()
    for instance in instances:
        instance.clean()


def test_section_copy(db):
    instances = Section.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.pages.count() == instance.pages.count()


def test_page_str(db):
    instances = Page.objects.all()
    for instance in instances:
        assert str(instance)


def test_page_clean(db):
    instances = Page.objects.all()
    for instance in instances:
        instance.clean()


def test_page_copy(db):
    instances = Page.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert new_instance.questionsets.count() == instance.questionsets.count()
        assert new_instance.questions.count() == instance.questions.count()


def test_questionset_str(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert str(instance)


def test_questionset_clean(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        instance.clean()


def test_questionset_copy(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert new_instance.questionsets.count() == instance.questionsets.count()
        assert new_instance.questions.count() == instance.questions.count()


def test_question_str(db):
    instances = Question.objects.all()
    for instance in instances:
        assert str(instance)


def test_question_clean(db):
    instances = Question.objects.all()
    for instance in instances:
        instance.clean()


def test_question_copy(db):
    instances = Question.objects.all()
    for instance in instances:
        new_uri_prefix = instance.uri_prefix + '-'
        new_key = instance.key + '-'
        new_instance = instance.copy(new_uri_prefix, new_key)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.key == new_key
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert list(new_instance.optionsets.values('id')) == list(instance.optionsets.values('id'))
