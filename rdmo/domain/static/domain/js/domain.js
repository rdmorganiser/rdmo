angular.module('domain', ['core'])

.factory('DomainService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        entities: $resource(baseurl + 'api/internal/domain/entities/:list_route/:id/'),
        attributes: $resource(baseurl + 'api/internal/domain/attributes/:list_route/:id/'),
        optionsets: $resource(baseurl + 'api/internal/domain/optionsets/:id/'),
        ranges: $resource(baseurl + 'api/internal/domain/ranges/:id/'),
        verbosenames: $resource(baseurl + 'api/internal/domain/verbosenames/:id/'),
        valuetypes: $resource(baseurl + 'api/internal/domain/valuetypes/:id/'),
        conditions: $resource(baseurl + 'api/internal/domain/conditions/:id/')
    };

    /* configure factories */

    var factories = {
        entities: function(parent) {
            var entity = {
                parent: null,
                is_collection: false
            };

            if (angular.isDefined(parent) && parent) {
                entity.parent = parent.id;
            }
            console.log(entity);
            return entity;
        },
        attributes: function(parent) {
            var attribute = {
                parent: null,
                is_collection: false,
                value_type: null
            };

            if (angular.isDefined(parent) && parent) {
                attribute.parent = parent.id;
            }

            return attribute;
        },
        ranges: function(parent) {
            return {
                attribute: parent.id
            };
        },
        verbosenames: function(parent) {
            return {
                attribute_entity: parent.id
            };
        }
    };


    /* create the domain service */

    var service = {};

    service.init = function(options) {
        service.valuetypes = resources.valuetypes.query();

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

        var domain_promise = resources.entities.query({list_route: 'nested'}, function(response) {
            service.domain = response;
        }).$promise;

        service.entities = resources.entities.query({list_route: 'index'});
        service.attributes = resources.attributes.query({list_route: 'index'});
        service.optionsets = resources.optionsets.query();
        service.conditions = resources.conditions.query();

        return $q.all([
            domain_promise,
            service.entities.$promise,
            service.attributes.$promise,
            service.optionsets.$promise,
            service.conditions.$promise
        ]);
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = null;
        service.values = null;
        service.current_object = obj;

        if (angular.isDefined(create) && create) {

            service.values = factories[resource](obj);

        } else {

            if (resource === 'verbosenames') {
                service.values = resources.verbosenames.query({attribute_entity: obj.id}, function(response) {
                    service.values = (response.length) ? response[0] : factories.verbosenames(obj);
                });
            } else if (resource === 'ranges') {
                service.values = resources.ranges.query({attribute: obj.id}, function(response) {
                    service.values = (response.length) ? response[0] : factories.ranges(obj);
                });
            } else if (resource === 'optionsets') {
                service.values = resources.attributes.get({id: obj.id});
            } else if (resource === 'conditions') {
                if (obj.is_attribute) {
                    service.values = resources.attributes.get({id: obj.id});
                } else {
                    service.values = resources.entities.get({id: obj.id});
                }
            } else {
                service.values = resources[resource].get({id: obj.id});
            }

        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {

        var promise;

        if (resource === 'optionsets') {
            promise = service.storeValues('attributes');
        } else if (resource === 'conditions') {
            if (service.current_object.is_attribute) {
                promise = service.storeValues('attributes');
            } else {
                promise = service.storeValues('entities');
            }
        } else {
            promise = service.storeValues(resource);
        }

        promise.then(function() {
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
            console.log(service.values.id);
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

    service.addOption = function() {
        service.values.push(factories.options(service.current_object));
    };

    return service;

}])

.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
