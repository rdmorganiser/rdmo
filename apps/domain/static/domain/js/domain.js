var app = angular.module('domain', ['select-by-number', 'formgroup']);

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

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'entities': baseurl + 'domain/api/entities/',
        'attribute': baseurl + 'domain/api/attributes/',
        'attributeset': baseurl + 'domain/api/attributesets/',
        'valuetypes': baseurl + 'domain/api/valuetypes/'
    };

    /* private methods */

    function fetchValueTypes() {
        $http.get(urls.valuetypes).success(function(response) {
            service.valuetypes = response;
        });
    }

    function fetchEntities() {
        $http.get(urls.entities).success(function(response) {
            service.entities = response;
            service.attributesets = [];

            angular.forEach(service.entities, function(entity) {
                if (entity.is_set) {
                    service.attributesets.push({
                        id: entity.id,
                        tag: entity.tag
                    });
                }
            });
        });
    }

    function fetchItem(type, id) {
        $http.get(urls[type] + id + '/')
            .success(function(response) {
                service.values = response;
            });
    }

    function createItem(type) {
        $http.post(urls[type], service.values)
            .success(function(response) {
                fetchEntities();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function updateItem(type) {
        $http.put(urls[type] + service.values.id + '/', service.values)
            .success(function(response) {
                fetchEntities();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function deleteItem(type) {
        $http.delete(urls[type] + service.values.id + '/', service.values)
            .success(function(response) {
                fetchEntities();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    /* public methods */

    service.init = function(options) {
        fetchValueTypes();
        fetchEntities();
    };

    service.openFormModal = function(type, obj) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(obj)) {
            if (type === 'attribute') {
                if (angular.isUndefined(obj.attributes)) {
                    fetchItem('attribute', obj.id);
                } else {
                    service.values.order = 0;
                    service.values.attributeset = obj.id;
                }
            } else if (type === 'attributeset') {
                fetchItem('attributeset', obj.id);
            }
        } else {
            service.values.is_collection = false;
        }

        $timeout(function() {
            $('#' + type + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(type) {
        if (angular.isUndefined(service.values.id)) {
            createItem(type);
        } else {
            updateItem(type);
        }
    };

    service.openDeleteModal = function(type, obj) {
        service.values = obj;
        $('#' + type + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(type) {
        deleteItem(type);
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
