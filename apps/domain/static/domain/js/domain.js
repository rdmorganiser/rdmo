var app = angular.module('domain', ['select-by-number']);

// customizations for Django integration
app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('DomainService', ['$http', '$timeout', function($http, $timeout) {

    var entities_url = '/domain/api/entities/',
        attributes_url = '/domain/api/attributes/',
        attributesets_url = '/domain/api/attributesets/';

    service = {
        values: {},
        errors: {},
        entities: [],
        sets: []
    };

    function fetchEntities() {
        $http.get(entities_url).success(function(response) {
            service.entities = response;
        });
    }

    function fetchSets() {
        $http.get(attributesets_url).success(function(response) {
            service.sets = response;
        });
    }

    function createEntity() {
        // decide on the url
        var url;
        if (service.values.is_set) {
            url = attributesets_url;
        } else {
            url = attributes_url;
        }

        // update the entity on the server
        $http.post(url, service.values)
            .success(function(response) {
                service.init();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function updateEntity() {
        // decide on the url
        var url;
        if (service.values.is_set) {
            url = attributesets_url + service.values.id + '/';
        } else {
            url = attributes_url + service.values.id + '/';
        }

        // update the entity on the server
        $http.put(url, service.values)
            .success(function(response) {
                service.init();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function deleteEntity() {
        // decide on the url
        var url;
        if (service.values.is_set) {
            url = attributesets_url + service.values.id + '/';
        } else {
            url = attributes_url + service.values.id + '/';
        }

        // update the entity on the server
        $http.delete(url)
            .success(function(response) {
                service.init();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    service.init = function(options) {
        fetchEntities();
        fetchSets();
    };

    service.openFormModal = function(action, entity) {

        if (action === 'create') {
            service.values = {
                'is_set': false,
                'is_collection': false,
                'attributeset': null
            };
        } else if (action === 'create-set') {
            service.values = {
                'is_set': true,
                'is_collection': false
            };
        } else if (action === 'add') {
            service.values = {
                'is_set': false,
                'is_collection': false,
                'attributeset': entity.id
            };
        } else if (action === 'update') {
            service.values = angular.copy(entity);
        }

        service.action = action;
        $('#form-modal').modal('show');
    };

    service.submitFormModal = function() {
        if (angular.isUndefined(service.values.id)) {
            createEntity();
        } else {
            updateEntity();
        }
    };

    service.openDeleteModal = function(action, entity) {
        service.values = angular.copy(entity);
        $('#delete-modal').modal('show');
    };

    service.submitDeleteModal = function() {
        service.deleteEntity();
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
