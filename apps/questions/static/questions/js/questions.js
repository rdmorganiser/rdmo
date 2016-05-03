var app = angular.module('questions', ['select-by-number', 'formgroup']);

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

    var service = {};

    /* private variables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'catalog': baseurl + 'api/questions/catalogs/',
        'section': baseurl + 'api/questions/sections/',
        'subsection': baseurl + 'api/questions/subsections/',
        'entity': baseurl + 'api/questions/entities/',
        'question': baseurl + 'api/questions/questions/',
        'questionset': baseurl + 'api/questions/questionsets/',
        'option': baseurl + 'api/questions/options/',
        'widgettype': baseurl + 'api/questions/widgettypes/',
        'attribute': baseurl + 'api/domain/attributes',
        'attributeset': baseurl + 'api/domain/attributesets'
    };

    /* private methods */

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
        $http.get(urls.widgettype).success(function(response) {
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
        $http.get(urls.catalog + service.catalogId + '/')
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

    function storeItem(type, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        if (angular.isUndefined(values.id)) {
            $http.post(urls[type], values)
                .success(function(response) {
                    if (type === 'catalog') {
                        service.catalogId = response.id;
                    } else if (type === 'question') {
                        angular.forEach(values.options, function(option) {
                            storeItem('option', option);
                        });
                    }
                    fetchCatalogs();
                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        } else {
            $http.put(urls[type] + values.id + '/', values)
                .success(function(response) {
                    if (type === 'question') {
                        angular.forEach(values.options, function(option) {
                            storeItem('option', option);
                        });
                    }
                    fetchCatalogs();
                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        }
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

    /* public methods */

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
                fetchAttributeSets();
                if (angular.isUndefined(obj.entities)) {
                    fetchItem('questionset', obj.id);
                } else {
                    service.values.order = 0;
                }
            } else if (type === 'question') {
                fetchAttributes();
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
                fetchAttributeSets();
                service.values.order = 0;
            } else if (type === 'question') {
                fetchAttributes();
                service.values.order = 0;
            }
        }

        $timeout(function() {
            $('#' + type + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(type) {
        storeItem(type);
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
