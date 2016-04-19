var app = angular.module('questions', ['select-by-number', 'form-fields']);

// customizations for Django integration
app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('QuestionsService', ['$http', '$timeout', function($http, $timeout) {

    var urls = {
        'catalog': '/questions/api/catalogs/',
        'section': '/questions/api/sections/',
        'subsection': '/questions/api/subsections/',
        'entities': '/questions/api/entities/',
        'question': '/questions/api/questions/',
        'questionset': '/questions/api/questionsets/',
        'widgettypes': '/questions/api/widgettypes/',
        'attribute': '/domain/api/attributes',
        'attributeset': '/domain/api/attributesets'
    };

    var service = {
        values: {},
        errors: {},
        catalogs: [],
        sections: [],
        subsections: [],
        questionsets: [],
        widget_types: [],

    };

    function fetchAttributes() {
        $http.get(urls.attribute).success(function(response) {
            service.attributes = response;
        });
    }

    function fetchAttributeSets() {
        $http.get(urls.attributeset).success(function(response) {
            service.attributesets = response;
        });
    }

    function fetchWidgetTypes() {
        $http.get(urls.widgettypes).success(function(response) {
            service.widget_types = response;
        });
    }

    function fetchCatalogs() {
        $http.get(urls.catalog).success(function(response) {
            service.catalogs = response;

            if (angular.isUndefined(service.catalogId) && angular.isDefined(response[0])) {
                service.catalogId = response[0].id;
            }

            if (angular.isDefined(service.catalogId)) {
                fetchCatalog();
            }
        });
    }

    function fetchCatalog() {
        $http.get(urls['catalog'] + service.catalogId + '/')
            .success(function(response) {
                service.catalog = response;
                service.sections = service.catalog.sections;
                service.subsections = [];
                service.questionsets = [];

                angular.forEach(service.sections, function(section) {
                    angular.forEach(section.subsections, function(subsection) {
                        service.subsections.push({
                            id: subsection.id,
                            title: subsection.title
                        });

                        angular.forEach(subsection.entities, function(entity) {
                            if (entity.is_set) {
                                service.questionsets.push({
                                    id: entity.id,
                                    title: entity.title
                                });
                            }
                        });
                    });
                });
            });
    }

    function fetchItem(type, id) {
        $http.get(urls[type] + id + '/')
            .success(function(response) {
                service.values = response;
            });
    }

    function createItem(type) {
        $http.post(urls[type], service.values)
            .success(function(response) {
                if (type === 'catalog') {
                    service.catalogId = response.id;
                }
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function updateItem(type) {
        $http.put(urls[type] + service.values.id + '/', service.values)
            .success(function(response) {
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function deleteItem(type) {
        $http.delete(urls[type] + service.values.id + '/', service.values)
            .success(function(response) {
                if (type === 'catalog') {
                    delete service.catalogId;
                    delete service.catalog;
                }
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    service.init = function() {
        fetchAttributes();
        fetchAttributeSets();
        fetchWidgetTypes();
        fetchCatalogs();
    };

    service.changeCatalog = function() {
        fetchCatalog();
    };

    service.openFormModal = function(type, obj) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(obj)) {
            if (type === 'catalog') {
                service.values = angular.copy(obj);
            } else if (type === 'section') {
                fetchItem('section', obj.id);
            } else if (type === 'subsection') {
                if (angular.isUndefined(obj.subsections)) {
                    fetchItem('subsection', obj.id);
                } else {
                    service.values.order = 0;
                }
            } else if (type === 'questionset') {
                if (angular.isUndefined(obj.entities)) {
                    fetchItem('questionset', obj.id);
                } else {
                    service.values.order = 0;
                }
            } else if (type === 'question') {
                if (angular.isUndefined(obj.entities)) {
                    fetchItem('question', obj.id);
                } else {
                    service.values.order = 0;
                }
            }
        } else {
            if (type === 'catalog') {
                // nothing to do, move along
            } else if (type === 'section') {
                service.values.order = 0;
                service.values.catalog = service.catalog.id;
            } else if (type === 'subsection') {
                service.values.order = 0;
            } else if (type === 'questionset') {
                service.values.order = 0;
            } else if (type === 'question') {
                service.values.order = 0;
            }
        }

        $timeout(function() {
            $('#' + type + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(type) {
        if (angular.isUndefined(service.values.id)) {
            createItem(type);
        } else {
            updateItem(type);
        }
    };

    service.openDeleteModal = function(type, obj) {
        service.values = obj;
        $('#' + type + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(type) {
        deleteItem(type);
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
