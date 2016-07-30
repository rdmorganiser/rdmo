var app = angular.module('tasks', ['core'])

.factory('TasksService', ['$resource', '$timeout', '$window', function($resource, $timeout, $window) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        tasks: $resource(baseurl + 'api/tasks/tasks/:route/:id/'),
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

        service.initTasks();

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initTasks = function(options) {
        resources.tasks.query({route: 'index'},function (response) {
            service.tasks = response;
        });
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
        var promise;

        if (angular.isDefined(service.values.id)) {
            if (resource === 'conditions') {
                promise = resources.tasks.update({
                    id: service.values.id
                }, service.values).$promise;
            } else {
                promise = resources[resource].update({
                    id: service.values.id
                }, service.values).$promise;
            }
        } else {
            if (resource === 'conditions') {
                promise = resources.tasks.save(service.values).$promise;
            } else {
                promise = resources[resource].save(service.values).$promise;
            }
        }

        promise.then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.initTasks();
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
            service.initTasks();
        });
    };

    return service;

}]);

app.controller('TasksController', ['$scope', 'TasksService', function($scope, TasksService) {

    $scope.service = TasksService;
    $scope.service.init();

}]);
