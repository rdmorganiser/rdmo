angular.module('questions', ['core'])

.factory('QuestionsService', ['$resource', '$timeout', '$window', '$q', function($resource, $timeout, $window, $q) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* configure resources */

    var resources = {
        catalogs: $resource(baseurl + 'api/questions/catalogs/:list_route/:id/:detail_route/'),
        sections: $resource(baseurl + 'api/questions/sections/:list_route/:id/'),
        subsections: $resource(baseurl + 'api/questions/subsections/:list_route/:id/'),
        questionsets: $resource(baseurl + 'api/questions/questionsets/:list_route/:id/'),
        questions: $resource(baseurl + 'api/questions/questions/:id/'),
        entities: $resource(baseurl + 'api/questions/entities/:id/'),
        attributes: $resource(baseurl + 'api/questions/attributes/:id/'),
        widgettypes: $resource(baseurl + 'api/questions/widgettypes/:id/'),
    };

    /* configure factories */

    var factories = {
        catalogs: function(parent) {
            return {
                order: 0
            };
        },
        sections: function(parent) {
            return {
                catalog: (angular.isDefined(parent) && parent) ? parent.id : null,
                order: 0
            };
        },
        subsections: function(parent) {
            return {
                section: (angular.isDefined(parent) && parent) ? parent.id : null,
                order: 0
            };
        },
        questionsets: function(parent) {
            return {
                subsection: (angular.isDefined(parent) && parent) ? parent.id : null,
                attribute_entity: null,
                order: 0
            };
        },
        questions: function(parent) {
            var question = {
                attribute_entity: null,
                order: 0
            };

            if (angular.isDefined(parent) && parent) {
                if (angular.isDefined(parent.is_set)) {
                    question.subsection = parent.subsection;
                    question.parent = parent.id;
                } else {
                    question.subsection = parent.id;
                    question.parent = null;
                }
            } else {
                question.subsection = null;
                question.parent = null;
            }

            return question;
        }
    };

    /* create the questions service */

    var service = {};

    service.init = function() {
        service.widgettypes = resources.widgettypes.query();
        service.entities = resources.entities.query();
        service.attributes = resources.attributes.query();

        resources.catalogs.query({list_route: 'index'}, function(response) {
            service.catalogs = response;
            service.current_catalog_id = service.catalogs[0].id;

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

        var catalog_promise = resources.catalogs.get({
            id: service.current_catalog_id,
            detail_route: 'nested'
        }, function(response) {
            service.catalog = response;
        }).$promise;

        service.sections = resources.sections.query({list_route: 'index'});
        service.subsections = resources.subsections.query({list_route: 'index'});
        service.questionsets = resources.questionsets.query({list_route: 'index'});

        return $q.all([
            catalog_promise,
            service.sections.$promise,
            service.subsections.$promise,
            service.questionsets.$promise
        ]);
    };

    service.openFormModal = function(resource, obj, create, copy) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(create) && create) {
            if (angular.isDefined(copy) && copy === true) {
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
        });
    };

    service.submitFormModal = function(resource) {
        service.storeValues(resource).then(function(response) {
            if (resource === 'catalogs') {
                resources.catalogs.query(function(catalogs) {
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
                resources.catalogs.query(function(catalogs) {
                    service.catalogs = catalogs;
                    service.current_catalog_id = service.catalogs[0].id;
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

.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
