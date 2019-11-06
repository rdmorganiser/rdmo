angular.module('views', ['core'])

.factory('ViewsService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        views: $resource(baseurl + 'api/v1/views/views/:list_action/:id/'),
        catalogs: $resource(baseurl + 'api/v1/questions/catalogs/index/'),
        settings: $resource(baseurl + 'api/v1/core/settings/'),
        sites: $resource(baseurl + 'api/v1/core/sites/'),
        groups: $resource(baseurl + 'api/v1/core/groups/'),
    };

    /* configure factories */

    var factories = {
        views: function(parent) {
            return {
                template: '',
                uri_prefix: service.settings.default_uri_prefix,
                sites: [1]
            };
        }
    };

    /* create the tasks service */

    var service = {};

    service.init = function(options) {
        service.catalogs = resources.catalogs.query();
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
        return resources.views.query({list_action: 'index'}, function(response) {
            service.views = response;
        }).$promise;
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};
        service.current_object = obj;

        if (angular.isDefined(create) && create) {
            service.values = factories['views'](obj);
        } else {
            service.values = resources['views'].get({id: obj.id});
        }

        $q.when(service.values.$promise).then(function() {
            if (service.values.template === ''){
                service.values.template = '{% load view_tags %}'
            };
            $('#' + resource + '-form-modal').modal('show');
            angular.element('.CodeMirror')[0].CodeMirror.refresh();
        });
    };

    service.submitFormModal = function(resource, close) {
        service.errors = {};

        if (angular.isDefined(service.editor)) {
            service.values.template = service.editor.getValue();
        }

        service.storeValues('views').then(function() {
            if (angular.isUndefined(close) || close) {
                $('#' + resource + '-form-modal').modal('hide');
                service.initView();
            }
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

.controller('ViewsController', ['$scope', 'ViewsService', function($scope, ViewsService) {

    $scope.service = ViewsService;
    $scope.service.init();

}]);
