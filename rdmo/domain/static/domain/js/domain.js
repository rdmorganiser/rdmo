angular.module('domain', ['core'])

.factory('DomainService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        attributes: $resource(baseurl + 'api/internal/domain/attributes/:list_route/:id/'),
        ranges: $resource(baseurl + 'api/internal/domain/ranges/:id/'),
        verbosenames: $resource(baseurl + 'api/internal/domain/verbosenames/:id/'),
        settings: $resource(baseurl + 'api/internal/domain/settings/'),
    };

    /* configure factories */

    var factories = {
        attributes: function(parent) {
            var attribute = {
                parent: null,
                uri_prefix: service.settings.default_uri_prefix
            };

            if (angular.isDefined(parent) && parent) {
                attribute.parent = parent.id;
            }

            return attribute;
        }
    };

    /* create the domain service */

    var service = {};

    service.init = function(options) {
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

    service.initView = function() {

        var domain_promise = resources.attributes.query({list_route: 'nested'}, function(response) {
            service.domain = response;
        }).$promise;

        service.attributes = resources.attributes.query({list_route: 'index'});

        return $q.all([
            domain_promise,
            service.attributes.$promise
        ]);
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = null;
        service.values = null;
        service.current_object = obj;

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
            $('.modal').modal('hide');
            service.current_object = null;
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
            $('.modal').modal('hide');
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

.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
