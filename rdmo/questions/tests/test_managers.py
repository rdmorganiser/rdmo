from ..models import Catalog, Question


def test_questions_filter_by_catalog(db):
    catalog = Catalog.objects.prefetch_elements().first()
    questions = Question.objects.filter_by_catalog(catalog)
    assert questions.count() == 97
