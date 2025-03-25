#import pytest

# from django.contrib.auth.models import User

# from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

# pytestmark = pytest.mark.django_db

# users = (
#     ("admin", HTTP_200_OK),
#     ("user", HTTP_200_OK),
#     ("anonymous", HTTP_302_FOUND),
# )


# @pytest.mark.parametrize("username,status_code", users)
# def test_openapi_schema(client, settings, username, status_code):
#     if username != "anonymous":
#         user = User.objects.get(username=username)
#         client.force_login(user)
#     response = client.get("/api/v1/")
#     assert response.status_code == status_code
#     # TODO check yaml response
#     # TODO check json response


# @pytest.mark.parametrize("username,status_code", users)
# def test_openapi_swagger_ui(client, username, status_code):
#     if username != "anonymous":
#         user = User.objects.get(username=username)
#         client.force_login(user)
#     response = client.get("/api/v1/swagger/")
#     assert response.status_code == status_code
#     if username != "anonymous":
#         # logged in user can access the swagger ui
#         assert '<div id="swagger-ui"></div>' in str(response.content)


# @pytest.mark.parametrize("username,status_code", users)
# def test_openapi_redoc_ui(client, username, status_code):
#     if username != "anonymous":
#         user = User.objects.get(username=username)
#         client.force_login(user)
#     response = client.get("/api/v1/redoc/")
#     assert response.status_code == status_code
#     if username != "anonymous":
#         # logged in user can access the redoc ui
#         assert '<redoc spec-url="/api/v1/"></redoc>' in str(response.content)
