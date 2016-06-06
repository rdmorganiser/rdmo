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
        'valuetypes': baseurl + 'api/domain/valuetypes/',
        'relations':  baseurl + 'api/domain/relations/'
    };

    /* private methods */

    function factory(ressource, parent) {
        if (ressource === 'entities' || ressource === 'attributes') {
            var item = {
                'parent_entity': null,
                'title': '',
                'description': '',
                'uri': '',
                'is_collection': false
            };

            if (angular.isDefined(parent) && parent) {
                item.parent_entity = parent.id;
            } else {
                item.parent_entity = null;
            }

            if (ressource === 'attributes') {
                item.value_type = null;
                item.unit = '';
            }

            return item;
        } else if (ressource === 'options') {
            return {
                'attribute': parent.id,
                'text_en': '',
                'text_de': '',
                'order': 0,
                'additional_input': false
            };
        } else if (ressource === 'ranges') {
            return {
                'attribute': parent.id,
                'minimum': 0,
                'maximum': 10,
                'step': 1
            };
        } else if (ressource === 'conditions') {
            return {
                'attribute': parent.id,
                'source_attribute': null,
                'relation': 'eq',
                'target_value': '',
                'target_option': null
            };
        }
    }

    function fetchValueTypes() {
        $http.get(urls.valuetypes).success(function(response) {
            service.valuetypes = response;
        });
    }

    function fetchRelations() {
        $http.get(urls.relations).success(function(response) {
            service.relations = response;
        });
    }

    function fetchEntities() {
        var config = {
            params: {
                nested: true
            }
        };
        var p1 = $http.get(urls.entities, config).success(function(response) {
            service.entities = response;
        });
        var p2 = $http.get(urls.entities).success(function(response) {
            service.entity_options = response;
        });
        var p3 = $http.get(urls.attributes).success(function(response) {
            service.attribute_options = response;
        });
        var p4 = $http.get(urls.options).success(function(response) {
            service.option_options = response;
        });

        return $q.all([p1, p2, p3, p4]);
    }

    function fetchItem(ressource, id) {
        return $http.get(urls[ressource] + id + '/').success(function(response) {
            service.values = response;
        });
    }

    function storeItem(ressource) {
        var promise;

        if (angular.isDefined(service.values.id)) {
            promise = $http.put(urls[ressource] + service.values.id + '/', service.values);
        } else {
            promise = $http.post(urls[ressource], service.values);
        }

        promise.error(function(response) {
            service.errors = response;
        });

        return promise;
    }

    function deleteItem(ressource) {
        return $http.delete(urls[ressource] + service.values.id + '/').error(function(response) {
            service.errors = response;
        });
    }

    function storeItems(ressource) {
        var promises = [];

        angular.forEach(service.values[ressource], function(item, index) {
            var promise = null;

            if (angular.isUndefined(item.attribute)) {
                item.attribute = service.values.id;
            }

            if (item.removed) {
                if (angular.isDefined(item.id)) {
                    promise = $http.delete(urls[ressource] + item.id + '/');
                }
            } else {
                if (angular.isDefined(item.id)) {
                    promise = $http.put(urls[ressource] + item.id + '/', item);
                } else {
                    promise = $http.post(urls[ressource], item);
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
    }

    /* public methods */

    service.init = function(options) {
        fetchValueTypes();
        fetchRelations();
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
            if (ressource === 'options' || ressource === 'conditions') {
                fetchItem('attributes', obj.id).then(function() {
                    service.values[ressource].push(factory(ressource, service.values));
                })
            } else {
                service.values = factory(ressource, obj);
            }
        } else {
            if (ressource === 'options' || ressource === 'conditions') {
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
        if (ressource === 'options' || ressource === 'conditions') {
            storeItems(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
                fetchEntities();
            });
        } else {
            storeItem(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
                fetchEntities();
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
            fetchEntities();
        });
    };

    service.addItem = function(ressource) {
        service.values[ressource].push(factory(ressource, service.values));
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
