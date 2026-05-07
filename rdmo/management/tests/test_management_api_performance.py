import pytest

from rdmo.management.constants import RDMO_MODEL_PATH_MAPPER

pytestmark = pytest.mark.django_db


MANAGEMENT_ENDPOINTS = {
    "conditions.condition": {
        "url": "/api/v1/conditions/conditions/",
        "queries": {
            "index": 3,
            "list": 9,
            "detail": 9,
        },
    },
    "domain.attribute": {
        "url": "/api/v1/domain/attributes/",
        "queries": {
            "index": 3,
            "list": 10,
            "detail": 11,
        },
    },
    "options.optionset": {
        "url": "/api/v1/options/optionsets/",
        "queries": {
            "index": 3,
            "list": 8,
            "detail": 8,
        },
    },
    "options.option": {
        "url": "/api/v1/options/options/",
        "queries": {
            "index": 3,
            "list": 10,
            "detail": 10,
        },
    },
    "questions.catalog": {
        "url": "/api/v1/questions/catalogs/",
        "queries": {
            "index": 3,
            "list": 8,
            "detail": 8,
        },
    },
    "questions.section": {
        "url": "/api/v1/questions/sections/",
        "queries": {
            "index": 3,
            "list": 8,
            "detail": 8,
        },
    },
    "questions.page": {
        "url": "/api/v1/questions/pages/",
        "queries": {
            "index": 3,
            "list": 10,
            "detail": 10,
        },
    },
    "questions.questionset": {
        "url": "/api/v1/questions/questionsets/",
        "queries": {
            "index": 3,
            "list": 11,
            "detail": 10,
        },
    },
    "questions.question": {
        "url": "/api/v1/questions/questions/",
        "queries": {
            "index": 3,
            "list": 10,
            "detail": 10,
        },
    },
    "tasks.task": {
        "url": "/api/v1/tasks/tasks/",
        "queries": {
            "index": 3,
            "list": 10,
            "detail": 10,
        },
    },
    "views.view": {
        "url": "/api/v1/views/views/",
        "queries": {
            "index": 3,
            "list": 8,
            "detail": 8,
        },
    },
}


def get_params(action):
    params = []

    for model_path, config in MANAGEMENT_ENDPOINTS.items():
        max_queries = config["queries"][action]

        if action == "index":
            url = f'{config["url"]}index/'
        else:
            url = config["url"]

        params.append(pytest.param(
            model_path,
            url,
            max_queries,
            id=f"{model_path}-{action}",
        ))

    return params


@pytest.mark.performance
@pytest.mark.parametrize(
    "model_path,url,max_queries",
    get_params("index"),
)
def test_management_index_endpoint_query_counts(
    admin_client,
    django_assert_max_num_queries,
    model_path,
    url,
    max_queries,
):
    assert model_path in RDMO_MODEL_PATH_MAPPER

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize(
    "model_path,url,max_queries",
    get_params("list"),
)
def test_management_list_endpoint_query_counts(
    admin_client,
    django_assert_max_num_queries,
    model_path,
    url,
    max_queries,
):
    assert model_path in RDMO_MODEL_PATH_MAPPER

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize(
    "model_path,url,max_queries",
    get_params("detail"),
)
def test_management_detail_endpoint_query_counts(
    admin_client,
    django_assert_max_num_queries,
    model_path,
    url,
    max_queries,
):
    model = RDMO_MODEL_PATH_MAPPER[model_path]
    obj = model.objects.first()

    assert obj is not None, f"No test object exists for {model_path}."

    with django_assert_max_num_queries(max_queries):
        response = admin_client.get(f"{url}{obj.pk}/")

    assert response.status_code == 200
