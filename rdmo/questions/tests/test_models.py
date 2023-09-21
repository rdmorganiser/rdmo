from ..models import Catalog, Page, Question, QuestionSet, Section


def test_catalog_str(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.uri


def test_catalog_property_is_locked(db):
    instances = Catalog.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked


def test_catalog_clean(db):
    instances = Catalog.objects.all()
    for instance in instances:
        instance.clean()


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

                page_elements = sorted([
                    *page.page_questionsets.all(),
                    *page.page_questions.all()
                ], key=lambda e: e.order)
                for page_element in page_elements:
                    element = page_element.element
                    descendant_ids.append(element.id)

                    try:
                        element_elements = sorted([
                            *element.questionset_questionsets.all(),
                            *element.questionset_questions.all()
                        ], key=lambda e: e.order)
                    except AttributeError:
                        element_elements = []

                    for element_element in element_elements:
                        element2 = element_element.element
                        descendant_ids.append(element2.id)

                        try:
                            element_elements2 = sorted([
                                *element2.questionset_questionsets.all(),
                                *element2.questionset_questions.all()
                            ], key=lambda e: e.order)
                        except AttributeError:
                            element_elements2 = []

                        for element_element2 in element_elements2:
                            descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_section_str(db):
    instances = Section.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.uri


def test_section_property_is_locked(db):
    instances = Section.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.catalog.is_locked


def test_section_clean(db):
    instances = Section.objects.all()
    for instance in instances:
        instance.clean()


def test_section_descendants(db):
    instances = Section.objects.all()
    for instance in instances:
        descendant_ids = []

        for section_page in instance.section_pages.order_by('order'):
            page = section_page.page
            descendant_ids.append(page.id)

            page_elements = sorted([
                *page.page_questionsets.all(),
                *page.page_questions.all()
            ], key=lambda e: e.order)
            for page_element in page_elements:
                element = page_element.element
                descendant_ids.append(element.id)

                try:
                    element_elements = sorted([
                        *element.questionset_questionsets.all(),
                        *element.questionset_questions.all()
                    ], key=lambda e: e.order)
                except AttributeError:
                    element_elements = []

                for element_element in element_elements:
                    element2 = element_element.element
                    descendant_ids.append(element2.id)

                    try:
                        element_elements2 = sorted([
                            *element2.questionset_questionsets.all(),
                            *element2.questionset_questions.all()
                        ], key=lambda e: e.order)
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


def test_page_descendants(db):
    instances = Page.objects.all()
    for instance in instances:
        descendant_ids = []

        page_elements = sorted([
            *instance.page_questionsets.all(),
            *instance.page_questions.all()
        ], key=lambda e: e.order)
        for page_element in page_elements:
            element = page_element.element
            descendant_ids.append(element.id)

            try:
                element_elements = sorted([
                    *element.questionset_questionsets.all(),
                    *element.questionset_questions.all()
                ], key=lambda e: e.order)
            except AttributeError:
                element_elements = []

            for element_element in element_elements:
                element2 = element_element.element
                descendant_ids.append(element2.id)

                try:
                    element_elements2 = sorted([
                        *element2.questionset_questionsets.all(),
                        *element2.questionset_questions.all()
                    ], key=lambda e: e.order)
                except AttributeError:
                    element_elements2 = []

                for element_element2 in element_elements2:
                    descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_questionset_str(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.uri


def test_questionset_property_is_locked(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.section.is_locked


def test_questionset_clean(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        instance.clean()


def test_questionset_descendants(db):
    instances = QuestionSet.objects.all()
    for instance in instances:
        descendant_ids = []

        try:
            element_elements = sorted([
                *instance.questionset_questionsets.all(),
                *instance.questionset_questions.all()
            ], key=lambda e: e.order)
        except AttributeError:
            element_elements = []

        for element_element in element_elements:
            element2 = element_element.element
            descendant_ids.append(element2.id)

            try:
                element_elements2 = sorted([
                    *element2.questionset_questionsets.all(),
                    *element2.questionset_questions.all()
                ], key=lambda e: e.order)
            except AttributeError:
                element_elements2 = []

            for element_element2 in element_elements2:
                descendant_ids.append(element_element2.element.id)

        assert [d.id for d in instance.descendants] == descendant_ids


def test_question_str(db):
    instances = Question.objects.all()
    for instance in instances:
        assert str(instance)
        assert str(instance) == instance.uri


def test_question_clean(db):
    instances = Question.objects.all()
    for instance in instances:
        instance.clean()


def test_question_property_is_locked(db):
    instances = Question.objects.all()
    for instance in instances:
        assert instance.is_locked == instance.locked or instance.questionset.is_locked
