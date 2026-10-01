import pytest

from django.urls import reverse

from ..models import OptionSet
from ..prefetch import optionset_options_prefetch
from ..viewsets import OptionSetViewSet
from .factories import create_options, create_optionset
from .test_viewset_optionsets import urlnames


def test_list_many_options(db, admin_client):
    options = list(reversed(create_options(1100, 'query-safety-list-option')))
    optionset = create_optionset('query-safety-list', options)

    response = admin_client.get(reverse(urlnames['list']), {'uri': optionset.uri})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['options'] == [
        {'option': option.pk, 'order': order}
        for order, option in enumerate(options)
    ]


def test_nested_many_options(db, admin_client):
    options = list(reversed(create_options(1100, 'query-safety-nested-option')))
    optionset = create_optionset('query-safety-nested', options)

    response = admin_client.get(reverse(urlnames['nested'], args=[optionset.pk]))

    assert response.status_code == 200
    data = response.json()
    assert [(element['id'], element['text']) for element in data['elements']] == [
        (option.pk, option.text_lang1) for option in options
    ]


@pytest.mark.performance
def test_prefetch_distributed_options(db, django_assert_max_num_queries, django_assert_num_queries):
    options = create_options(1100, 'query-safety-distributed-option')
    expected_options = {}
    for index in range(4):
        selected_options = list(reversed(options[index * 275:(index + 1) * 275]))
        optionset = create_optionset(f'query-safety-distributed-{index}', selected_options)
        expected_options[optionset.pk] = [(option.pk, order) for order, option in enumerate(selected_options)]

    with django_assert_max_num_queries(2):
        optionsets = list(OptionSet.objects.filter(pk__in=expected_options).prefetch_related(
            optionset_options_prefetch('optionset_options')
        ))

    with django_assert_num_queries(0):
        actual_options = {
            optionset.pk: [(optionset_option.option.pk, optionset_option.order)
                           for optionset_option in optionset.optionset_options.all()]
            for optionset in optionsets
        }

    assert actual_options == expected_options


@pytest.mark.performance
def test_prefetch_shared_options(db, django_assert_max_num_queries, django_assert_num_queries):
    options = list(reversed(create_options(6, 'query-safety-shared-option')))
    optionsets = [create_optionset(f'query-safety-shared-{index}', options) for index in range(4)]
    expected_options = {
        optionset.pk: [(option.pk, order) for order, option in enumerate(options)]
        for optionset in optionsets
    }

    with django_assert_max_num_queries(2):
        optionsets = list(OptionSet.objects.filter(pk__in=expected_options).prefetch_related(
            optionset_options_prefetch('optionset_options')
        ))

    with django_assert_num_queries(0):
        actual_options = {
            optionset.pk: [(optionset_option.option.pk, optionset_option.order)
                           for optionset_option in optionset.optionset_options.all()]
            for optionset in optionsets
        }

    assert actual_options == expected_options


@pytest.mark.performance
def test_prefetch_many_optionsets(db, django_assert_max_num_queries, django_assert_num_queries):
    options = create_options(80, 'query-safety-many-optionsets-option')
    expected_options = {}
    for index, option in enumerate(options):
        optionset = create_optionset(f'query-safety-many-optionsets-{index}', [option])
        expected_options[optionset.pk] = [(option.pk, 0)]

    with django_assert_max_num_queries(2):
        optionsets = list(OptionSet.objects.filter(pk__in=expected_options).prefetch_related(
            optionset_options_prefetch('optionset_options')
        ))

    with django_assert_num_queries(0):
        actual_options = {
            optionset.pk: [(optionset_option.option.pk, optionset_option.order)
                           for optionset_option in optionset.optionset_options.all()]
            for optionset in optionsets
        }

    assert actual_options == expected_options


@pytest.mark.performance
@pytest.mark.parametrize('option_count', [4, 40])
def test_prefetch_query_count(db, django_assert_num_queries, option_count):
    options = list(reversed(create_options(option_count, 'query-safety-query-count-option')))
    optionset = create_optionset('query-safety-query-count', options)
    expected_options = [(option.pk, order) for order, option in enumerate(options)]

    with django_assert_num_queries(2):
        optionset = OptionSet.objects.prefetch_related(
            optionset_options_prefetch('optionset_options')
        ).get(pk=optionset.pk)

    with django_assert_num_queries(0):
        actual_options = [(optionset_option.option.pk, optionset_option.order)
                          for optionset_option in optionset.optionset_options.all()]

    assert actual_options == expected_options


@pytest.mark.performance
@pytest.mark.parametrize('action,expected_queries', [('list', 1), ('nested', 0)])
def test_optionset_queryset_option_queries(db, django_assert_num_queries, action, expected_queries):
    options = create_options(3, 'query-safety-action-option')
    optionset = create_optionset('query-safety-action', options)
    view = OptionSetViewSet()
    view.action = action
    optionset = view.get_queryset().get(pk=optionset.pk)

    with django_assert_num_queries(expected_queries):
        option_uri = optionset.optionset_options.all()[0].option.uri

    assert option_uri == options[0].uri
