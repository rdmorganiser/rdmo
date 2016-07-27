var app = angular.module('domain', ['core', 'select-by-number', 'formgroup']);

// customizations for Django integration
app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('DomainService', ['$http', '$timeout', '$window', '$q', 'ResourcesService', function($http, $timeout, $window, $q, ResourcesService) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* create the domain service */

    var service = {};

    /* create and configure the resource service */

    var resources = ResourcesService;

    resources.urls = {
        'entities': baseurl + 'api/domain/entities/',
        'attributes': baseurl + 'api/domain/attributes/',
        'options': baseurl + 'api/domain/options/',
        'ranges': baseurl + 'api/domain/ranges/',
        'conditions': baseurl + 'api/domain/conditions/',
        'verbosenames': baseurl + 'api/domain/verbosenames/',
        'valuetypes': baseurl + 'api/domain/valuetypes/'
    };

    resources.service = service;

    resources.factory = function(resource, parent) {
        if (resource === 'entities' || resource === 'attributes') {
            var entity = {
                'parent_entity': null,
                'title': '',
                'description': '',
                'uri': '',
                'is_collection': false
            };
            console.log(parent);
            if (angular.isDefined(parent) && parent) {
                entity.parent_entity = parent.id;
            } else {
                entity.parent_entity = null;
            }

            if (resource === 'attributes') {
                entity.value_type = null;
                entity.unit = '';
            }

            return entity;
        } else if (resource === 'options') {
            return {
                'attribute': parent.id,
                'text_en': '',
                'text_de': '',
                'order': 0,
                'additional_input': false
            };
        } else if (resource === 'ranges') {
            return {
                'attribute': parent.id,
                'minimum': 0,
                'maximum': 10,
                'step': 1
            };
        } else if (resource === 'conditions') {
            return {
                'id': parent.id,
                'source_attribute': null,
                'relation': 'eq',
                'target_value': '',
                'target_option': null
            };
        } else if (resource === 'verbosenames') {
            return {
                'attribute_entity': parent.id,
                'name_en': '',
                'name_de': '',
                'name_plural_en': '',
                'name_plural_de': '',
            };
        }
    };

    /* configure the domain service */

    service.init = function(options) {
        resources.fetchItems('valuetypes');

        service.initDomain().then(function () {
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

    service.initDomain = function() {
        var promises = [];

        promises.push($http.get(resources.urls.entities + 'nested/').success(function(response) {
            service.domain = response;
        }));

        promises.push(resources.fetchItems('entities'));
        promises.push(resources.fetchItems('attributes'));
        promises.push(resources.fetchItems('options'));
        promises.push(resources.fetchItems('conditions'));

        return $q.all(promises);
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = null;
        service.values = null;
        service.current_object = obj;

        if (angular.isDefined(create) && create) {

            if (resource === 'options') {
                service.values = [resources.factory(resource, obj)];
            } else if (resource === 'conditions') {
                if (obj.is_attribute) {
                    resources.fetchItem('attributes', obj.id);
                } else {
                    resources.fetchItem('entities', obj.id);
                }
            } else {
                service.values = resources.factory(resource, obj);
            }

        } else {

            if (resource === 'options') {
                $http.get(resources.urls[resource], {
                    params: {
                        attribute: obj.id
                    }
                }).success(function (response) {
                    service.values = response;
                });
            } else if (resource === 'conditions') {
                if (obj.is_attribute) {
                    resources.fetchItem('attributes', obj.id);
                } else {
                    resources.fetchItem('entities', obj.id);
                }
            } else {
                resources.fetchItem(resource, obj.id);
            }

        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        var promise;

        if (resource === 'options') {

            service.errors = [];
            promise = resources.storeItems(resource);

        } else if (resource === 'conditions') {

            service.errors = {};
            if (service.current_object.is_attribute) {
                promise = resources.storeItem('attributes');
            } else {
                promise = resources.storeItem('entities');
            }

        } else {

            service.errors = {};
            resources.storeItem(resource);

        }

        promise.then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.current_object = null;
            service.initDomain();
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources.deleteItem(resource).then(function() {
            $('#' + resource + '-delete-modal').modal('hide');
            service.initDomain();
        });
    };

    service.addItem = function(resource) {
        service.values.push(resources.factory(resource, service.current_object));
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
