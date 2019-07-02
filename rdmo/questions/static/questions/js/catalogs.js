angular.module('catalogs', ['core'])

.config(['$locationProvider', function($locationProvider) {

    // set $location to not use #
    $locationProvider.html5Mode(true);

}])

.factory('CatalogsService', ['$resource', '$timeout', '$window', '$q', '$location', function($resource, $timeout, $window, $q, $location) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        catalogs: $resource(baseurl + 'api/v1/questions/catalogs/:list_action/:id/:detail_action/'),
        sections: $resource(baseurl + 'api/v1/questions/sections/:list_action/:id/'),
        questionsets: $resource(baseurl + 'api/v1/questions/questionsets/:list_action/:id/'),
        questions: $resource(baseurl + 'api/v1/questions/questions/:id/'),
        widgettypes: $resource(baseurl + 'api/v1/questions/widgettypes/:id/'),
        valuetypes: $resource(baseurl + 'api/v1/questions/valuetypes/:id/'),
        attributes: $resource(baseurl + 'api/v1/domain/attributes/:id/'),
        optionsets: $resource(baseurl + 'api/v1/options/optionsets/:id/'),
        conditions: $resource(baseurl + 'api/v1/conditions/conditions/:id/'),
        settings: $resource(baseurl + 'api/v1/core/settings/'),
        sites: $resource(baseurl + 'api/v1/core/sites/'),
        groups: $resource(baseurl + 'api/v1/core/groups/'),
    };

    /* configure factories */

    var factories = {
        catalogs: function(parent) {
            return {
                order: 0,
                sites: [1],
                uri_prefix: service.settings.default_uri_prefix
            };
        },
        sections: function(parent) {
            return {
                catalog: (angular.isDefined(parent) && parent) ? parent.id : null,
                order: 0,
                uri_prefix: service.settings.default_uri_prefix
            };
        },
        questionsets: function(parent) {
            return {
                section: (angular.isDefined(parent) && parent) ? parent.id : null,
                attribute: null,
                order: 0,
                uri_prefix: service.settings.default_uri_prefix
            };
        },
        questions: function(parent) {
            return {
                questionset: (angular.isDefined(parent) && parent) ? parent.id : null,
                attribute: null,
                order: 0,
                uri_prefix: service.settings.default_uri_prefix
            };
        }
    };

    /* create the questions service */

    var service = {};

    service.init = function() {
        service.widgettypes = resources.widgettypes.query();
        service.valuetypes = resources.valuetypes.query();
        service.attributes = resources.attributes.query();
        service.optionsets = resources.optionsets.query();
        service.conditions = resources.conditions.query();
        service.settings = resources.settings.get();
        service.sites = resources.sites.query();
        service.groups = resources.groups.query();

        resources.catalogs.query({list_action: 'index'}, function(response) {
            service.catalogs = response;

            // try to get the catalog from the address bar
            var catalog_id = $location.path().replace(/\//g,'');

            if (catalog_id) {
                service.current_catalog_id = catalog_id;
            } else if (service.catalogs.length) {
                service.current_catalog_id = service.catalogs[0].id;
            } else {
                service.current_catalog_id = null;
            }

            service.initView().then(function() {
                var current_scroll_pos = sessionStorage.getItem('current_scroll_pos');
                if (current_scroll_pos) {
                    $timeout(function() {
                        $window.scrollTo(0, current_scroll_pos);
                    });
                }
            });

        });

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initView = function() {
        if (service.current_catalog_id) {
            $location.path('/' + service.current_catalog_id + '/');

            service.sections = resources.sections.query({list_action: 'index'});
            service.questionsets = resources.questionsets.query({list_action: 'index'});

            var catalog_promise = resources.catalogs.get({
                id: service.current_catalog_id,
                detail_action: 'nested'
            }, function(response) {
                service.catalog = response;
            }).$promise;

            return $q.all([
                service.sections.$promise,
                service.questionsets.$promise,
                catalog_promise
            ]);
        } else {
            return $q.resolve();
        }
    };

    service.openFormModal = function(resource, obj, create, copy) {
        service.errors = {};
        service.values = {};
        service.copy = false;

        if (angular.isDefined(create) && create) {
            if (angular.isDefined(copy) && copy === true) {
                service.copy = true;
                service.values = resources[resource].get({id: obj.id}, function() {
                    delete service.values.id;
                });
            } else {
                service.values = factories[resource](obj);
            }
        } else {
            service.values = resources[resource].get({id: obj.id});
        }

        $q.when(service.values.$promise).then(function() {
            $('#' + resource + '-form-modal').modal('show');
            $('formgroup[data-quicksearch="true"]').trigger('refresh');
        });
    };

    service.submitFormModal = function(resource) {
        service.storeValues(resource).then(function(response) {
            if (resource === 'catalogs') {
                resources.catalogs.query({list_action: 'index'}, function(catalogs) {
                    service.catalogs = catalogs;
                    service.current_catalog_id = response.id;
                    service.initView();
                });
            } else {
                service.initView();
            }

            $('#' + resource + '-form-modal').modal('hide');
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
            if (resource === 'catalogs') {
                resources.catalogs.query({list_action: 'index'}, function(catalogs) {
                    service.catalogs = catalogs;

                    if (service.catalogs.length) {
                        service.current_catalog_id = service.catalogs[0].id;
                    } else {
                        service.current_catalog_id = null;
                    }

                    service.initView();
                });
            } else {
                service.initView();
            }

            $('#' + resource + '-delete-modal').modal('hide');
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

.controller('CatalogsController', ['$scope', 'CatalogsService', function($scope, CatalogsService) {

    $scope.service = CatalogsService;
    $scope.service.init();

}]);
