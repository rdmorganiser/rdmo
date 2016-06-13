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
        'valuetypes': baseurl + 'api/domain/valuetypes/',
        'relations':  baseurl + 'api/domain/relations/'
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
                'attribute': parent.id,
                'source_attribute': null,
                'relation': 'eq',
                'target_value': '',
                'target_option': null
            };
        }
    };

    resources.fetchDomain = function() {
        var promises = [];

        promises.push($http.get(resources.urls.entities, {
            params: {
                nested: true
            }
        }).success(function(response) {
            service.domain = response;
        }));

        promises.push(resources.fetchItems('entities'));
        promises.push(resources.fetchItems('attributes'));
        promises.push(resources.fetchItems('options'));

        return $q.all(promises);
    };

    /* configure the domain service */

    service.init = function(options) {
        resources.fetchItems('valuetypes');
        resources.fetchItems('relations');

        resources.fetchDomain().then(function () {
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
                resources.fetchItem('attributes', obj.id).then(function() {
                    service.values[ressource].push(resources.factory(ressource, service.values));
                });
            } else {
                service.values = resources.factory(ressource, obj);
            }
        } else {
            if (ressource === 'options' || ressource === 'conditions') {
                resources.fetchItem('attributes', obj.id);
            } else {
                resources.fetchItem(ressource, obj.id);
            }
        }

        $timeout(function() {
            $('#' + ressource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(ressource) {
        if (ressource === 'options' || ressource === 'conditions') {
            resources.storeItems(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
                resources.fetchDomain();
            });
        } else {
            resources.storeItem(ressource).then(function() {
                $('#' + ressource + '-form-modal').modal('hide');
                resources.fetchDomain();
            });
        }
    };

    service.openDeleteModal = function(ressource, obj) {
        service.values = obj;
        $('#' + ressource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(ressource) {
        resources.deleteItem(ressource).then(function() {
            $('#' + ressource + '-delete-modal').modal('hide');
            service.fetchDomain();
        });
    };

    service.addItem = function(ressource) {
        service.values[ressource].push(resources.factory(ressource, service.values));
    };

    return service;

}]);

app.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
