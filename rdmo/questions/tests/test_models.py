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
        assert list(new_instance.sections.values('id')) == list(instance.sections.values('id'))


def test_catalog_descendants(db):
    instances = Catalog.objects.all()
    for instance in instances:
        descendant_ids = []

        for section in instance.sections.order_by('order'):
            descendant_ids.append(section.id)

            for page in section.pages.order_by('order'):
                descendant_ids.append(page.id)

                elements = list(page.questionsets.all()) + list(page.questions.all())
                for element in sorted(elements, key=lambda e: e.order):
                    descendant_ids.append(element.id)

                    try:
                        elements2 = list(element.questionsets.all()) + list(element.questions.all())
                    except AttributeError:
                        elements2 = []

                    for element2 in sorted(elements2, key=lambda e: e.order):
                        descendant_ids.append(element2.id)

                        try:
                            elements3 = list(element2.questionsets.all()) + list(element2.questions.all())
                        except AttributeError:
                            elements3 = []

                        for element3 in sorted(elements3, key=lambda e: e.order):
                            descendant_ids.append(element3.id)

        assert [d.id for d in instance.descendants] == descendant_ids


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
        new_uri_path = instance.uri_path + '-'
        new_instance = instance.copy(new_uri_prefix, new_uri_path)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.uri_path == new_uri_path
        assert list(new_instance.pages.values('id')) == list(instance.pages.values('id'))


def test_section_descendants(db):
    instances = Section.objects.all()
    for instance in instances:
        descendant_ids = []

        for page in instance.pages.order_by('order'):
            descendant_ids.append(page.id)

            elements = list(page.questionsets.all()) + list(page.questions.all())
            for element in sorted(elements, key=lambda e: e.order):
                descendant_ids.append(element.id)

                try:
                    elements2 = list(element.questionsets.all()) + list(element.questions.all())
                except AttributeError:
                    elements2 = []

                for element2 in sorted(elements2, key=lambda e: e.order):
                    descendant_ids.append(element2.id)

                    try:
                        elements3 = list(element2.questionsets.all()) + list(element2.questions.all())
                    except AttributeError:
                        elements3 = []

                    for element3 in sorted(elements3, key=lambda e: e.order):
                        descendant_ids.append(element3.id)

        assert [d.id for d in instance.descendants] == descendant_ids


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
        new_uri_path = instance.uri_path + '-'
        new_instance = instance.copy(new_uri_prefix, new_uri_path)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.uri_path == new_uri_path
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert list(new_instance.questionsets.values('id')) == list(instance.questionsets.values('id'))
        assert list(new_instance.questions.values('id')) == list(instance.questions.values('id'))


def test_page_descendants(db):
    instances = Page.objects.all()
    for instance in instances:
        descendant_ids = []

        try:
            elements = list(instance.questionsets.all()) + list(instance.questions.all())
        except AttributeError:
            elements = []

        for element in sorted(elements, key=lambda e: e.order):
            descendant_ids.append(element.id)

            try:
                elements2 = list(element.questionsets.all()) + list(element.questions.all())
            except AttributeError:
                elements2 = []

            for element2 in sorted(elements2, key=lambda e: e.order):
                descendant_ids.append(element2.id)

                try:
                    elements3 = list(element2.questionsets.all()) + list(element2.questions.all())
                except AttributeError:
                    elements3 = []

                for element3 in sorted(elements3, key=lambda e: e.order):
                    descendant_ids.append(element3.id)

        assert [d.id for d in instance.descendants] == descendant_ids


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
        new_uri_path = instance.uri_path + '-'
        new_instance = instance.copy(new_uri_prefix, new_uri_path)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.uri_path == new_uri_path
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert list(new_instance.questionsets.values('id')) == list(instance.questionsets.values('id'))
        assert list(new_instance.questions.values('id')) == list(instance.questions.values('id'))


def test_questionset_descendants(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        descendant_ids = []

        try:
            elements = list(instance.questionsets.all()) + list(instance.questions.all())
        except AttributeError:
            elements = []

        for element in sorted(elements, key=lambda e: e.order):
            descendant_ids.append(element.id)

            try:
                elements2 = list(element.questionsets.all()) + list(element.questions.all())
            except AttributeError:
                elements2 = []

            for element2 in sorted(elements2, key=lambda e: e.order):
                descendant_ids.append(element2.id)

        assert [d.id for d in instance.descendants] == descendant_ids


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
        new_uri_path = instance.uri_path + '-'
        new_instance = instance.copy(new_uri_prefix, new_uri_path)
        assert new_instance.uri_prefix == new_uri_prefix
        assert new_instance.uri_path == new_uri_path
        assert new_instance.attribute == instance.attribute
        assert list(new_instance.conditions.values('id')) == list(instance.conditions.values('id'))
        assert list(new_instance.optionsets.values('id')) == list(instance.optionsets.values('id'))
