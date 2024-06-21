import pytest

from rdmo.projects.models import Project
from rdmo.projects.progress import compute_navigation

sections = (
    'http://example.com/terms/questions/catalog/individual',
    'http://example.com/terms/questions/catalog/collections',
    'http://example.com/terms/questions/catalog/set',
    'http://example.com/terms/questions/catalog/conditions',
    'http://example.com/terms/questions/catalog/blocks'
)

# (count, total, show) for each page or section (as default fallback)
result_map = {
    'http://example.com/terms/questions/catalog/individual': (8, 9),
    'http://example.com/terms/questions/catalog/individual/*': (1, 1, True),
    'http://example.com/terms/questions/catalog/individual/autocomplete': (0, 1, True),
    'http://example.com/terms/questions/catalog/collections': (9, 10),
    'http://example.com/terms/questions/catalog/collections/*': (1, 1, True),
    'http://example.com/terms/questions/catalog/collections/autocomplete': (0, 1, True),
    'http://example.com/terms/questions/catalog/set': (47, 57),
    'http://example.com/terms/questions/catalog/set/individual-single': (8, 9, True),
    'http://example.com/terms/questions/catalog/set/individual-collection': (9, 10, True),
    'http://example.com/terms/questions/catalog/set/collection-single': (14, 18, True),
    'http://example.com/terms/questions/catalog/set/collection-collection': (16, 20, True),
    'http://example.com/terms/questions/catalog/conditions': (15, 23),
    'http://example.com/terms/questions/catalog/conditions/input': (2, 2, True),
    'http://example.com/terms/questions/catalog/conditions/text_contains': (1, 1, True),
    'http://example.com/terms/questions/catalog/conditions/text_empty': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/text_equal': (1, 1, True),
    'http://example.com/terms/questions/catalog/conditions/text_greater_than': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/text_greater_than_equal': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/text_lesser_than': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/text_lesser_than_equal': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/text_not_empty': (1, 1, True),
    'http://example.com/terms/questions/catalog/conditions/text_not_equal': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/option_empty': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/option_equal': (1, 1, True),
    'http://example.com/terms/questions/catalog/conditions/option_not_empty': (1, 1, True),
    'http://example.com/terms/questions/catalog/conditions/option_not_equal': (1, 1, False),
    'http://example.com/terms/questions/catalog/conditions/set': (0, 2, True),
    'http://example.com/terms/questions/catalog/conditions/set_set': (0, 2, True),
    'http://example.com/terms/questions/catalog/conditions/optionset': (0, 2, True),
    'http://example.com/terms/questions/catalog/conditions/text_set': (0, 2, True),
    'http://example.com/terms/questions/catalog/blocks': (9, 12),
    'http://example.com/terms/questions/catalog/blocks/set': (9, 12, True),
}


@pytest.mark.parametrize('section_uri', sections)
def test_compute_navigation(db, section_uri):
    project = Project.objects.get(id=1)
    project.catalog.prefetch_elements()

    section = project.catalog.sections.get(uri=section_uri)

    navigation = compute_navigation(section, project)
    assert [item['id'] for item in navigation] == [element.id for element in project.catalog.elements]

    for section in navigation:
        if section['uri'] in result_map:
            count, total = result_map[section['uri']]
            assert section['count'] == count, section['uri']
            assert section['total'] == total, section['uri']

        if 'pages' in section:
            for page in section['pages']:
                uri = page['uri']
                wildcard_uri = section['uri'] + '/*'

                if uri in result_map:
                    count, total, show = result_map[uri]
                elif wildcard_uri in result_map:
                    count, total, show = result_map[wildcard_uri]
                else:
                    raise AssertionError('{uri} not in result_map'.format(**page))

                assert page['count'] == count, page['uri']
                assert page['total'] == total, page['uri']
                assert page['show'] == show, page['uri']
