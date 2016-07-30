angular.module('core', ['ngResource', 'select-by-number', 'formgroup'])

// customizations for Django integration
.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.config(['$resourceProvider', function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $resourceProvider.defaults.actions.update = {
        method: 'PUT',
        params: {}
    };
}])

.factory('ResourcesService', ['$http', '$q', function($http, $q) {

    var resources = {};

    function _store(resource, item) {
        var promise;

        if (angular.isDefined(item.removed) && item.removed) {
            if (angular.isDefined(item.id)) {
                promise = $http.delete(resources.urls[resource] + item.id + '/');
            }
        } else {
            if (angular.isDefined(item.id)) {
                promise = $http.put(resources.urls[resource] + item.id + '/', item);
            } else {
                promise = $http.post(resources.urls[resource], item);
            }
        }

        return promise;
    }

    resources.fetchItem = function(resource, id) {
        return $http.get(resources.urls[resource] + id + '/')
            .success(function(response) {
                resources.service.values = response;
            });
    };

    resources.fetchItems = function(resource, config) {
        if (angular.isUndefined(config)) {
            config = {};
        }

        return $http.get(resources.urls[resource], config)
            .success(function(response) {
                resources.service[resource] = response;
            });
    };

    resources.storeItem = function(resource) {
        var promise = _store(resource, resources.service.values);

        if (promise) {
            promise.error(function(response) {
                resources.service.errors = response;
            });
        }

        return promise;
    };

    resources.storeItems = function(resource) {
        var promises = [];

        angular.forEach(resources.service.values, function(item, index) {
            var promise = _store(resource, item, index);

            if (promise) {
                promise.error(function(response) {
                    resources.service.errors[index] = response;
                });
                promises.push(promise);
            }
        });

        return $q.all(promises);
    };

    resources.deleteItem = function(resource) {
        return $http.delete(resources.urls[resource] + resources.service.values.id + '/');
    };

    return resources;
}]);
