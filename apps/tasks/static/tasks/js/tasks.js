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
        'attributes': baseurl + 'api/domain/attributes/',
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
            service.values = resources.factory(resource, obj);
        } else {
            resources.fetchItem(resource, obj.id);
        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        resources.storeItem(resource).then(function() {
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
