angular.module('conditions', ['core'])

.factory('ConditionsService', ['$resource', '$timeout', '$window', '$q', '$filter', function($resource, $timeout, $window, $q, $filter) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        conditions: $resource(baseurl + 'api/v1/conditions/conditions/:list_route/:id/'),
        relations: $resource(baseurl + 'api/v1/conditions/relations/:id/'),
        attributes: $resource(baseurl + 'api/v1/domain/attributes/:id/'),
        options: $resource(baseurl + 'api/v1/options/options/:id/'),
        settings: $resource(baseurl + 'api/v1/core/settings/'),
    };

    /* configure factories */

    var factories = {
        conditions: function(parent) {
            return {
                source: null,
                relation: null,
                target_option: null,
                uri_prefix: service.settings.default_uri_prefix
            };
        }
    };

    /* create the conditions service */

    var service = {};

    service.init = function(options) {
        service.attributes = resources.attributes.query();
        service.options = resources.options.query();
        service.relations = resources.relations.query();
        service.settings = resources.settings.get();

        service.initView().then(function () {
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

    service.initView = function(options) {
        return resources.conditions.query({list_route: 'index'}, function(response) {
            service.conditions = response;
        }).$promise;
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(create) && create) {
            service.values = factories[resource](obj);
        } else {
            service.values = resources[resource].get({id: obj.id});
        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
            $('formgroup[data-quicksearch="true"]').trigger('refresh');
        });
    };

    service.submitFormModal = function(resource) {
        service.storeValues(resource).then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.initView();
        }, function(result) {
            service.errors = result.data;
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources[resource].delete({id: service.values.id}, function() {
            $('#' + resource + '-delete-modal').modal('hide');
            service.initView();
        });
    };

    service.storeValues = function(resource, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        if (angular.isDefined(values.removed) && values.removed) {
            if (angular.isDefined(values.id)) {
                return resources[resource].delete({id: values.id}).$promise;
            }
        } else {
            if (angular.isDefined(values.id)) {
                return resources[resource].update({id: values.id}, values).$promise;
            } else {
                return resources[resource].save(values).$promise;
            }
        }
    };

    return service;

}])

.controller('ConditionsController', ['$scope', 'ConditionsService', function($scope, ConditionsService) {

    $scope.service = ConditionsService;
    $scope.service.init();

}]);
