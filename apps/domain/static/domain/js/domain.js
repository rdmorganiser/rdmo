angular.module('domain', ['core'])

.factory('DomainService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        entities: $resource(baseurl + 'api/domain/entities/:list_route/:id/'),
        attributes: $resource(baseurl + 'api/domain/attributes/:id/'),
        options: $resource(baseurl + 'api/domain/options/:id/'),
        ranges: $resource(baseurl + 'api/domain/ranges/:id/'),
        verbosenames: $resource(baseurl + 'api/domain/verbosenames/:id/'),
        valuetypes: $resource(baseurl + 'api/domain/valuetypes/:id/'),
        conditions: $resource(baseurl + 'api/domain/conditions/:id/')
    };

    /* configure factories */

    var factories = {
        entities: function(parent) {
            var entity = {
                parent_entity: null,
                is_collection: false
            };

            if (angular.isDefined(parent) && parent) {
                entity.parent_entity = parent.id;
            }
            console.log(entity);
            return entity;
        },
        attributes: function(parent) {
            var attribute = {
                parent_entity: null,
                is_collection: false,
                value_type: null
            };

            if (angular.isDefined(parent) && parent) {
                attribute.parent_entity = parent.id;
            }

            return attribute;
        },
        options: function(parent) {
            return {
                attribute: parent.id,
                order: 0,
                additional_input: false
            };
        },
        ranges: function(parent) {
            return {
                attribute: parent.id,
                minimum: 0,
                maximum: 10,
                step: 1
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

        service.entities = resources.entities.query();
        service.attributes = resources.attributes.query();
        service.options = resources.options.query();
        service.conditions = resources.conditions.query();

        return $q.all([
            domain_promise,
            service.entities.$promise,
            service.attributes.$promise,
            service.options.$promise,
            service.conditions.$promise
        ]);
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = null;
        service.values = null;
        service.current_object = obj;

        console.log(resource, obj, create);

        if (angular.isDefined(create) && create) {

            if (resource === 'conditions') {
                if (obj.is_attribute) {
                    service.values = resources.attributes.get({id: obj.id});
                } else {
                    service.values = resources.entities.get({id: obj.id});
                }
            } else if (resource === 'options') {
                service.values = [factories[resource](obj)];
            } else {
                service.values = factories[resource](obj);
            }

        } else {

            if (resource === 'conditions') {
                if (obj.is_attribute) {
                    service.values = resources.attributes.get({id: obj.id});
                } else {
                    service.values = resources.entities.get({id: obj.id});
                }
            } else if (resource === 'options') {
                service.values = resources.options.query({attribute: obj.id});
            } else {
                service.values = resources[resource].get({id: obj.id});
            }

        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {

        if (resource === 'options') {
            service.errors = [];

            var promises = [];
            angular.forEach(service.values, function(option, index) {
                promises.push(service.storeValues('options', option).catch(function(result) {
                    service.errors[index] = result.data;
                    return $q.reject();
                }));
            });

            $q.all(promises).then(function() {
                $('#' + resource + '-form-modal').modal('hide');
                service.current_object = null;
                service.initView();
            });

        } else {
            var promise;

            if (resource === 'conditions') {
                if (service.current_object.is_attribute) {
                    promise = service.storeValues('attributes');
                } else {
                    promise = service.storeValues('entities');
                }
            } else {
                promise = service.storeValues(resource);
            }

            promise.then(function() {
                $('#' + resource + '-form-modal').modal('hide');
                service.current_object = null;
                service.initView();
            }, function(result) {
                service.errors = result.data;
            });
        }
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

    service.addOption = function() {
        service.values.push(factories.options(service.current_object));
    };

    return service;

}])

.controller('DomainController', ['$scope', 'DomainService', function($scope, DomainService) {

    $scope.service = DomainService;
    $scope.service.init();

}]);
