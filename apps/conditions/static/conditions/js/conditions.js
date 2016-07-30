var app = angular.module('conditions', ['core', 'select-by-number', 'formgroup', 'ngResource'])

.config(['$resourceProvider', function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $resourceProvider.defaults.actions.update = {
        method: 'PUT',
        params: {}
    };
}])

.factory('ConditionsService', ['$http', '$resource', '$timeout', '$window', '$q', function($http, $resource, $timeout, $window, $q, ResourcesService) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* create the domain service */

    var service = {};

    /* configure resources */

    var resources = {
        'conditions': $resource(baseurl + 'api/conditions/conditions/:route/:id/'),
        'attributes': $resource(baseurl + 'api/conditions/attributes/:id/'),
        'options': $resource(baseurl + 'api/conditions/options/:id/'),
        'relations': $resource(baseurl + 'api/conditions/relations/:id/')
    };

    /* configure factories */

    var factories = {
        'conditions': function(parent) {
            return {
                'source': null,
                'relation': null,
                'target_option': null
            };
        }
    };

    /* configure the domain service */

    service.init = function(options) {
        service.attributes = resources.attributes.query();
        service.options = resources.options.query();
        service.relations = resources.relations.query();

        service.initConditions();

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initConditions = function(options) {
        return resources.conditions.query({route: 'index'},function (response) {
            service.conditions = response;
        }).$promise;
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};
        service.current_object = obj;

        if (angular.isDefined(create) && create) {
            service.values = factories[resource](obj);
        } else {
            service.values = resources[resource].get({id: obj.id});
        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        var promise;

        if (angular.isDefined(service.values.id)) {
            promise = resources[resource].update({id: service.values.id}, service.values).$promise;
        } else {
            promise = resources[resource].save(service.values).$promise;
        }

        promise.then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.initConditions();
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources[resource].delete({id: service.values.id}, function() {
            $('#' + resource + '-delete-modal').modal('hide');
            service.initConditions();
        });
    };

    return service;

}])

.controller('ConditionsController', ['$scope', 'ConditionsService', function($scope, ConditionsService) {

    $scope.service = ConditionsService;
    $scope.service.init();

}]);
