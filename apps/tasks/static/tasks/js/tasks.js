angular.module('tasks', ['core'])

.factory('TasksService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        tasks: $resource(baseurl + 'api/internal/tasks/tasks/:list_route/:id/'),
        timeframes: $resource(baseurl + 'api/internal/tasks/timeframes/:id/'),
        attributes: $resource(baseurl + 'api/internal/tasks/attributes/:id/'),
        conditions: $resource(baseurl + 'api/internal/tasks/conditions/:id/')
    };

    /* configure factories */

    var factories = {
        tasks: function(parent) {
            return {
                attribute: null
            };
        },
        timeframes: function(task) {
            return {
                task: task.id,
                start_attribute: null,
                end_attribute: null
            }
        }
    };

    /* create the tasks service */

    var service = {};

    service.init = function(options) {
        service.attributes = resources.attributes.query();
        service.conditions = resources.conditions.query();

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
        return resources.tasks.query({list_route: 'index'}, function(response) {
            service.tasks = response;
        }).$promise;
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};
        service.current_object = obj;

        if (angular.isDefined(create) && create) {

            service.values = factories[resource](obj);

        } else {

            if (resource === 'timeframes') {
                service.values = resources.timeframes.query({task: obj.id}, function(response) {
                    // get the time frame from the response or create a new one
                    service.values = (response.length) ? response[0] : factories.timeframes(obj);
                });
            } else if (resource === 'conditions') {
                service.values = resources.tasks.get({id: obj.id});
            } else {
                service.values = resources[resource].get({id: obj.id});
            }

        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        var submit_resource = (resource === 'conditions') ? 'tasks': resource;

        service.storeValues(submit_resource).then(function() {
            $('.modal').modal('hide');
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
        if (angular.isDefined(service.values.id)) {
            resources[resource].delete({id: service.values.id}, function() {
                $('.modal').modal('hide');
                service.initView();
            });
        } else {
            $('.modal').modal('hide');
        }
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
