angular.module('options', ['core'])

.factory('OptionsService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        optionsets: $resource(baseurl + 'api/options/optionsets/:list_route/:id/'),
    };

    /* configure factories */

    var factories = {
        optionssets: function() {
            return {};
        },
        options: function(parent) {
            return {};
        }
    };

    /* create the options service */

    var service = {};

    service.init = function(options) {
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
        return resources.optionsets.query({list_route: 'index'}, function(response) {
            service.optionsets = response;
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

.controller('OptionsController', ['$scope', 'OptionsService', function($scope, OptionsService) {

    $scope.service = OptionsService;
    $scope.service.init();

}]);
