angular.module('tasks', ['core'])

.factory('TasksService', ['$resource', '$timeout', '$window', function($resource, $timeout, $window) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        tasks: $resource(baseurl + 'api/tasks/tasks/:list_route/:id/'),
        attributes: $resource(baseurl + 'api/tasks/attributes/:id/'),
        conditions: $resource(baseurl + 'api/tasks/conditions/:id/')
    };

    /* configure factories */

    var factories = {
        tasks: function(parent) {
            return {
                attribute: null
            };
        }
    };

    /* create the tasks service */

    var service = {};

    service.init = function(options) {
        service.attributes = resources.attributes.query();
        service.conditions = resources.conditions.query();

        service.initView();

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initView = function(options) {
        return resources.tasks.query({list_route: 'index'}, function(response) {
            service.tasks = response;
        }).$promise;
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};
        service.current_object = obj;

        if (angular.isDefined(create) && create) {
            if (resource === 'conditions') {
                service.values = resources.tasks.get({id: obj.id});
            } else {
                service.values = factories[resource](obj);
            }
        } else {
            if (resource === 'conditions') {
                service.values = resources.tasks.get({id: obj.id});
            } else {
                service.values = resources[resource].get({id: obj.id});
            }
        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        var submit_resource = (resource === 'conditions') ? 'tasks': resource;

        service.storeValues(submit_resource).then(function() {
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

.controller('TasksController', ['$scope', 'TasksService', function($scope, TasksService) {

    $scope.service = TasksService;
    $scope.service.init();

}]);
