var app = angular.module('tasks', ['core', 'select-by-number', 'formgroup']);

app.factory('TasksService', ['$http', '$timeout', '$window', '$q', 'ResourcesService', function($http, $timeout, $window, $q, ResourcesService) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* create the domain service */

    var service = {};

    /* create and configure the resource service */

    var resources = ResourcesService;

    resources.urls = {
        'tasks': baseurl + 'api/tasks/tasks/',
        'attributes': baseurl + 'api/tasks/attributes/',
        'conditions': baseurl + 'api/tasks/conditions/',
    };

    resources.service = service;

    resources.factory = function(resource, parent) {
        if (resource === 'tasks') {
            return {
                'attribute': null
            };
        }
    };

    /* configure the domain service */

    service.init = function(options) {
        resources.fetchItems('attributes');
        resources.fetchItems('conditions');

        service.initTasks();

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initTasks = function(options) {
        return $http.get(resources.urls['tasks'] + 'index/').success(function(response) {
            service.tasks = response;
        });
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(create) && create) {
            if (resource === 'conditions') {
                resources.fetchItem('tasks', obj.id);
            } else {
                service.values = resources.factory(resource, obj);
            }
        } else {
            if (resource === 'conditions') {
                resources.fetchItem('tasks', obj.id);
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

        if (resource === 'conditions') {
            promise = resources.storeItem('tasks');
        } else {
            promise = resources.storeItem(resource);
        }

        promise.then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.initTasks();
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources.deleteItem(resource).then(function() {
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
