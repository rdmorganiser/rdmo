angular.module('tasks', ['core'])

.factory('TasksService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        tasks: $resource(baseurl + 'api/v1/tasks/tasks/:list_action/:id/'),
        attributes: $resource(baseurl + 'api/v1/domain/attributes/:id/'),
        conditions: $resource(baseurl + 'api/v1/conditions/conditions/:id/'),
        settings: $resource(baseurl + 'api/v1/core/settings/'),
        sites: $resource(baseurl + 'api/v1/core/sites/'),
        groups: $resource(baseurl + 'api/v1/core/groups/'),
    };

    /* configure factories */

    var factories = {
        tasks: function(parent) {
            return {
                uri_prefix: service.settings.default_uri_prefix,
                attribute: null,
                sites: [1]
            };
        }
    };

    /* create the tasks service */

    var service = {};

    service.init = function(options) {
        service.attributes = resources.attributes.query();
        service.conditions = resources.conditions.query();
        service.settings = resources.settings.get();
        service.sites = resources.sites.query();
        service.groups = resources.groups.query();

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
        return resources.tasks.query({list_action: 'index'}, function(response) {
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
            service.values = resources.tasks.get({id: obj.id});
        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
            $('formgroup[data-quicksearch="true"]').trigger('refresh');
        });
    };

    service.submitFormModal = function(resource) {
        service.storeValues(resource).then(function() {
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
