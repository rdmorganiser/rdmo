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

app.factory('DomainService', ['$http', '$timeout', '$window', function($http, $timeout, $window) {

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'entities': baseurl + 'api/domain/entities/',
        'attribute': baseurl + 'api/domain/attributes/',
        'attributeset': baseurl + 'api/domain/attributesets/',
        'valuetypes': baseurl + 'api/domain/valuetypes/'
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
                        tag: entity.tag,
                        text: entity.text
                    });
                }
            });

            var current_scroll_pos = sessionStorage.getItem('current_scroll_pos');
            if (current_scroll_pos) {
                $timeout(function() {
                    $window.scrollTo(0, current_scroll_pos);
                });
            }
        });
    }

    function fetchItem(type, id) {
        $http.get(urls[type] + id + '/')
            .success(function(response) {
                service.values = response;
            });
    }

    function storeItem(type, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        if (angular.isUndefined(values.id)) {
            $http.post(urls[type], values)
                .success(function(response) {
                    fetchEntities();
                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        } else {
            $http.put(urls[type] + values.id + '/', values)
                .success(function(response) {
                    fetchEntities();
                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        }
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

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.openFormModal = function(type, obj) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(obj)) {
            if (type === 'attribute') {
                if (angular.isUndefined(obj.attributes) || obj.attributes === null) {
                    fetchItem('attribute', obj.id);
                } else {
                    service.values.order = 0;
                    service.values.is_collection = 0;
                    service.values.attributeset = obj.id;
                }
            } else if (type === 'attributeset') {
                fetchItem('attributeset', obj.id);
            }
        } else {
            service.values.attributeset = null;
            service.values.is_collection = false;
        }

        $timeout(function() {
            $('#' + type + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(type) {
        storeItem(type);

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
