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

app.factory('DomainService', ['$http', '$timeout', '$window', '$q', function($http, $timeout, $window, $q) {

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'entities': baseurl + 'api/domain/entities/',
        'attributes': baseurl + 'api/domain/attributes/',
        'options': baseurl + 'api/domain/options/',
        'ranges': baseurl + 'api/domain/ranges/',
        'conditions': baseurl + 'api/domain/conditions/',
        'valuetypes': baseurl + 'api/domain/valuetypes/'
    };

    /* private methods */

    function fetchValueTypes() {
        $http.get(urls.valuetypes).success(function(response) {
            service.valuetypes = response;
        });
    }

    function fetchEntities() {
        var config = {
            params: {
                nested: true
            }
        };
        var p1 = $http.get(urls.entities).success(function(response) {
            service.entity_options = response;
        });
        var p2 = $http.get(urls.entities, config).success(function(response) {
            service.entities = response;
        });

        return $q.all([p1, p2]);
    }

    function fetchItem(ressource, id) {
        $http.get(urls[ressource] + id + '/')
            .success(function(response) {
                service.values = response;
            });
    }

    function storeItem(ressource) {
        if (angular.isUndefined(service.values.id)) {
            return $http.post(urls[ressource], service.values)
                .error(function(response, status) {
                    service.errors = response;
                });
        } else {
            return $http.put(urls[ressource] + service.values.id + '/', service.values)
                .error(function(response, status) {
                    service.errors = response;
                });
        }
    }

    function storeItems(ressource) {

    }


    function deleteItem(ressource) {
        $http.delete(urls[ressource] + service.values.id + '/', service.values)
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
        fetchEntities().then(function () {
            var current_scroll_pos = sessionStorage.getItem('current_scroll_pos');
            if (current_scroll_pos) {
                $timeout(function() {
                    $window.scrollTo(0, current_scroll_pos);
                });
            }
        });

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.openFormModal = function(ressource, obj, create) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(create) && create) {
            if (angular.isDefined(obj) && obj) {
                service.values.parent_entity = obj.id;
            } else {
                service.values.parent_entity = null;
            }
            service.values.is_collection = false;
        } else {
            if (ressource === 'options') {
                fetchItem('attributes', obj.id);
            } else {
                fetchItem(ressource, obj.id);
            }
        }

        $timeout(function() {
            $('#' + ressource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(ressource) {
        if (ressource === 'entities' || ressource === 'attributes') {
            storeItem(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
            });
        } else {
            storeItems(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
            });
        }
    };

    service.openDeleteModal = function(ressource, obj) {
        service.values = obj;
        $('#' + ressource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(ressource) {
        deleteItem(ressource).then(function() {
            $('#' + ressource + '-delete-modal').modal('hide');
        });
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
