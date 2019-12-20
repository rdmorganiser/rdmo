from ..models import Catalog, Question, QuestionSet, Section


def test_catalog_str(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert str(instance)


def test_catalog_clean(db):
    instances = Catalog.objects.all()
    for instance in instances:
        instance.clean()


def test_section_str(db):
    instances = Section.objects.all()
    for instance in instances:
        assert str(instance)


def test_section_clean(db):
    instances = Section.objects.all()
    for instance in instances:
        instance.clean()


def test_questionset_str(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert str(instance)


def test_questionset_clean(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        instance.clean()


def test_question_str(db):
    instances = Question.objects.all()
    for instance in instances:
        assert str(instance)


def test_question_clean(db):
    instances = Question.objects.all()
    for instance in instances:
        instance.clean()
