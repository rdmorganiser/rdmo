angular.module('core', [])

// customizations for Django integration
.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.factory('BaseService', ['$http', '$q', function($http, $q) {

    return {
        fetchItem: function(ressource, id) {
            return $http.get(service.urls[ressource] + id + '/')
                .success(function(response) {
                    service.values = response;
                });
        },
        fetchItems: function(ressource) {
            return $http.get(service.urls[ressource])
                .success(function(response) {
                    service[ressource] = response;
                });
        },
        storeItem: function(ressource) {
            var promise;

            if (angular.isDefined(service.values.removed) && service.values.removed) {
                if (angular.isDefined(service.values.id)) {
                    promise = $http.delete(service.urls[ressource] + item.id + '/');
                }
            } else {
                if (angular.isDefined(service.values.id)) {
                    promise = $http.put(service.urls[ressource] + service.values.id + '/', service.values);
                } else {
                    promise = $http.post(service.urls[ressource], service.values);
                }
            }

            if (promise) {
                promise.error(function(response) {
                    service.errors = response;
                });
            }

            return promise;
        },
        storeItems: function(ressource) {
            var promises = [];

            angular.forEach(service.values[ressource], function(item, index) {
                var promise = null;

                if (angular.isDefined(item.removed) && item.removed) {
                    if (angular.isDefined(item.id)) {
                        promise = $http.delete(service.urls[ressource] + item.id + '/');
                    }
                } else {
                    if (angular.isDefined(item.id)) {
                        promise = $http.put(service.urls[ressource] + item.id + '/', item);
                    } else {
                        promise = $http.post(service.urls[ressource], item);
                    }
                }

                if (promise) {
                    promise.error(function(response) {
                        service.errors[index] = response;
                    });

                    promises.push(promise);
                }
            });

            return $q.all(promises);
        },
        deleteOne: function(ressource) {
            return $http.delete(service.urls[ressource] + service.values.id + '/');
        }
    };
}]);
