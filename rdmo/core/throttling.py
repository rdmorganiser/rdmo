from rest_framework.throttling import UserRateThrottle


class EmailThrottle(UserRateThrottle):
    scope = 'email'

    def allow_request(self, request, view):
        return request.method == 'GET' or super().allow_request(request, view)
