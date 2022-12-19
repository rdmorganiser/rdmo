from ..models import Catalog, Question


def test_questions_filter_by_catalog(db):
    catalog = Catalog.objects.prefetch_related(
        'sections__pages__questionsets',
        'sections__pages__questionsets__questions',
        'sections__pages__questions'
    ).first()
    questions = Question.objects.filter_by_catalog(catalog)
    assert questions.count() == 89
