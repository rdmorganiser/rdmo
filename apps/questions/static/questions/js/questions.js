var app = angular.module('questions', ['core', 'select-by-number', 'formgroup']);

// customizations for Django integration
app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('QuestionsService', ['$http', '$timeout', '$window', '$q', 'ResourcesService', function($http, $timeout, $window, $q, ResourcesService) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* create the domain service */

    var service = {};

    /* create and configure the resource service */

    var resources = ResourcesService;

    resources.urls = {
        'catalogs': baseurl + 'api/questions/catalogs/',
        'sections': baseurl + 'api/questions/sections/',
        'subsections': baseurl + 'api/questions/subsections/',
        'entities': baseurl + 'api/questions/entities/',
        'questions': baseurl + 'api/questions/questions/',
        'widgettypes': baseurl + 'api/questions/widgettypes/',
        'attribute_entities': baseurl + 'api/domain/entities/',
        'attributes': baseurl + 'api/domain/attributes/',
        'options': baseurl + 'api/domain/options/',
        'ranges': baseurl + 'api/domain/ranges/',
        'conditions': baseurl + 'api/domain/conditions/',
        'valuestypes': baseurl + 'api/domain/valuestypes/',
        'relations': baseurl + 'api/domain/relations/',
    };

    resources.service = service;

    resources.factory = function(resource, parent) {
        if (resource === 'catalogs') {
            return {
                'order': 0,
                'title_en': '',
                'title_de': ''
            };
        } else if (resource === 'sections') {
            var section = {
                'order': 0,
                'title_en': '',
                'title_de': ''
            };

            if (angular.isDefined(parent) && parent) {
                section.catalog = parent.id;
            } else {
                section.catalog = null;
            }

            return section;
        } else if (resource === 'subsections') {
            var subsection = {
                'order': 0,
                'title_en': '',
                'title_de': ''
            };

            if (angular.isDefined(parent) && parent) {
                subsection.section = parent.id;
            } else {
                subsection.section = null;
            }

            return subsection;
        } else if (resource === 'entities') {
            var entity = {
                'attribute_entity': null,
                'order': 0,
                'help_en': '',
                'help_de': ''
            };

            if (angular.isDefined(parent) && parent) {
                entity.subsection = parent.id;
            } else {
                entity.subsection = null;
            }

            return entity;
        } else if (resource === 'questions') {
            var question = {
                'attribute_entity': null,
                'order': 0,
                'text_en': '',
                'text_de': '',
                'help_en': '',
                'help_de': '',
                'widget_type': service.widgettypes[0].id
            };

            if (angular.isDefined(parent) && parent) {
                if (angular.isDefined(parent.is_set)) {
                    question.subsection = parent.subsection;
                    question.parent_entity = parent.id;
                } else {
                    question.subsection = parent.id;
                    question.parent_entity = null;
                }
            } else {
                question.subsection = null;
                question.parent_entity = null;
            }

            return question;
        }
    };

    /* configure the domain service */

    service.init = function() {

        resources.fetchItems('widgettypes');
        resources.fetchItems('attribute_entities');
        resources.fetchItems('attributes');

        resources.fetchItems('catalogs').then(function(result) {
            service.current_catalog_id = service.catalogs[0].id;

            service.initQuestions().then(function() {
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

    service.initQuestions = function() {
        var promises = [];

        promises.push(resources.fetchItems('sections'));
        promises.push(resources.fetchItems('subsections'));
        promises.push(resources.fetchItems('entities'));

        promises.push($http.get(resources.urls.catalogs + service.current_catalog_id + '/nested/')
            .success(function(response) {
                service.catalog = response;
            }));

        return $q.all(promises);
    };

    service.openFormModal = function(resource, obj, create, copy) {
        service.errors = {};
        service.values = {};
        service.current_object = obj;

        if (angular.isDefined(create) && create) {
            if (angular.isDefined(copy) && copy === true) {
                resources.fetchItem(resource, obj.id).then(function() {
                    delete service.values.id;
                });
            } else {
                service.values = resources.factory(resource, obj);
            }
        } else {
            resources.fetchItem(resource, obj.id);
        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        resources.storeItem(resource).then(function(result) {
            if (resource === 'catalogs') {
                var new_catalog_id = result.data.id;
                resources.fetchItems('catalogs').then(function(result) {
                    service.current_catalog_id = new_catalog_id;
                    service.initQuestions();
                });
            } else {
                service.initQuestions();
            }

            $('#' + resource + '-form-modal').modal('hide');
            service.current_object = null;
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources.deleteItem(resource).then(function(result) {
            if (resource === 'catalogs') {
                resources.fetchItems('catalogs').then(function(result) {
                    service.current_catalog_id = service.catalogs[0].id;
                    service.initQuestions();
                });
            } else {
                service.initQuestions();
            }

            $('#' + resource + '-delete-modal').modal('hide');
            service.current_object = null;
        });
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
