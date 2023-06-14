from ..models import Catalog, Page, Question, QuestionSet, Section


def test_catalog_str(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.key


def test_catalog_property_is_locked(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked


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

        for catalog_section in instance.catalog_sections.order_by('order'):
            section = catalog_section.section
            descendant_ids.append(section.id)

            for section_page in section.section_pages.order_by('order'):
                page = section_page.page
                descendant_ids.append(page.id)

                page_elements = list(page.page_questionsets.all()) + list(page.page_questions.all())
                page_elements = sorted(page_elements, key=lambda e: e.order)
                for page_element in page_elements:
                    element = page_element.element
                    descendant_ids.append(element.id)

                    try:
                        element_elements = list(element.questionset_questionsets.all()) + list(element.questionset_questions.all())
                        element_elements = sorted(element_elements, key=lambda e: e.order)
                    except AttributeError:
                        element_elements = []

                    for element_element in element_elements:
                        element2 = element_element.element
                        descendant_ids.append(element2.id)

                        try:
                            element_elements2 = list(element2.questionset_questionsets.all()) + list(element2.questionset_questions.all())
                            element_elements2 = sorted(element_elements2, key=lambda e: e.order)
                        except AttributeError:
                            element_elements2 = []

                        for element_element2 in element_elements2:
                            descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_section_str(db):
    instances = Section.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.path

def test_section_property_is_locked(db):
    instances = Section.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.catalog.is_locked


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

        for section_page in instance.section_pages.order_by('order'):
            page = section_page.page
            descendant_ids.append(page.id)

            page_elements = list(page.page_questionsets.all()) + list(page.page_questions.all())
            page_elements = sorted(page_elements, key=lambda e: e.order)
            for page_element in page_elements:
                element = page_element.element
                descendant_ids.append(element.id)

                try:
                    element_elements = list(element.questionset_questionsets.all()) + list(element.questionset_questions.all())
                    element_elements = sorted(element_elements, key=lambda e: e.order)
                except AttributeError:
                    element_elements = []

                for element_element in element_elements:
                    element2 = element_element.element
                    descendant_ids.append(element2.id)

                    try:
                        element_elements2 = list(element2.questionset_questionsets.all()) + list(element2.questionset_questions.all())
                        element_elements2 = sorted(element_elements2, key=lambda e: e.order)
                    except AttributeError:
                        element_elements2 = []

                    for element_element2 in element_elements2:
                        descendant_ids.append(element_element2.element.id)

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

        page_elements = list(instance.page_questionsets.all()) + list(instance.page_questions.all())
        page_elements = sorted(page_elements, key=lambda e: e.order)
        for page_element in page_elements:
            element = page_element.element
            descendant_ids.append(element.id)

            try:
                element_elements = list(element.questionset_questionsets.all()) + list(element.questionset_questions.all())
                element_elements = sorted(element_elements, key=lambda e: e.order)
            except AttributeError:
                element_elements = []

            for element_element in element_elements:
                element2 = element_element.element
                descendant_ids.append(element2.id)

                try:
                    element_elements2 = list(element2.questionset_questionsets.all()) + list(element2.questionset_questions.all())
                    element_elements2 = sorted(element_elements2, key=lambda e: e.order)
                except AttributeError:
                    element_elements2 = []

                for element_element2 in element_elements2:
                    descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_questionset_str(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.path


def test_questionset_property_is_locked(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.section.is_locked


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
            element_elements = list(instance.questionset_questionsets.all()) + list(instance.questionset_questions.all())
            element_elements = sorted(element_elements, key=lambda e: e.order)
        except AttributeError:
            element_elements = []

        for element_element in element_elements:
            element2 = element_element.element
            descendant_ids.append(element2.id)

            try:
                element_elements2 = list(element2.questionset_questionsets.all()) + list(element2.questionset_questions.all())
                element_elements2 = sorted(element_elements2, key=lambda e: e.order)
            except AttributeError:
                element_elements2 = []

            for element_element2 in element_elements2:
                descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_question_str(db):
    instances = Question.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.path


def test_question_clean(db):
    instances = Question.objects.all()
    for instance in instances:
        instance.clean()


def test_questionset_property_is_locked(db):
    instances = Question.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.questionset.is_locked


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
