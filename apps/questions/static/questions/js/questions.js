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

app.factory('QuestionsService', ['$http', '$timeout', '$window', function($http, $timeout, $window) {

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
        'condition': baseurl + 'api/questions/conditions/',
        'relation': baseurl + 'api/questions/relations/',
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

    function fetchRelations() {
        $http.get(urls.relation).success(function(response) {
            service.relations = response;
        });
    }

    function fetchCatalogs() {
        return $http.get(urls.catalog).success(function(response) {
            service.catalogs = response;
        });
    }

    function fetchCatalog() {
        return $http.get(urls.catalog + service.catalogId + '/')
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

    function fetchItem(type, id, copy) {
        $http.get(urls[type] + id + '/')
            .success(function(response) {
                service.values = response;

                if (angular.isDefined(copy) && copy === true) {
                    delete service.values.id;

                    angular.forEach(service.values.options, function(option) {
                        delete option.id;
                    });

                    angular.forEach(service.values.conditions, function(condition) {
                        delete condition.id;
                    });
                }
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
                        fetchCatalogs();
                    } else if (type === 'questionset') {
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('condition', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('condition', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (type === 'question') {
                        angular.forEach(values.options, function(option) {
                            if (option.removed === true) {
                                deleteItem('option', option);
                            } else {
                                option.question = response.id;
                                if (angular.isUndefined(option.input_field)) {
                                    option.input_field = false;
                                }
                                storeItem('option', option);
                            }
                        });
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('condition', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('condition', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (type === 'option' || type === 'condition') {
                        // pass
                    } else {
                        fetchCatalog();
                    }

                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        } else {
            $http.put(urls[type] + values.id + '/', values)
                .success(function(response) {
                    if (type === 'catalog') {
                        service.catalogId = response.id;
                        fetchCatalogs();
                    } else if (type === 'questionset') {
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('condition', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('condition', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (type === 'question') {
                        angular.forEach(values.options, function(option) {
                            if (option.removed === true) {
                                deleteItem('option', option);
                            } else {
                                option.question = response.id;
                                if (angular.isUndefined(option.input_field)) {
                                    option.input_field = false;
                                }
                                storeItem('option', option);
                            }
                        });
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('condition', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('condition', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (type === 'option' || type === 'condition') {
                        // pass
                    } else {
                        fetchCatalog();
                    }

                    $('.modal').modal('hide');
                })
                .error(function(response, status) {
                    service.errors = response;
                });
        }
    }

    function deleteItem(type, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        $http.delete(urls[type] + values.id + '/')
            .success(function(response) {
                if (type === 'catalog') {
                    delete service.catalogId;
                    delete service.catalog;
                    fetchCatalogs();
                } else if (type === 'option') {
                    // pass
                } else {
                    fetchCatalog();
                }

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
        fetchRelations();
        fetchCatalogs().then(function () {
            service.catalogId = service.catalogs[0].id;

            fetchCatalog().then(function() {
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

    service.changeCatalog = function() {
        fetchCatalog();
    };

    service.openFormModal = function(type, obj, copy) {

        service.errors = {};
        service.values = {};

        if (angular.isDefined(obj)) {
            if (type === 'catalog') {
                service.values = angular.copy(obj);
            } else if (type === 'section') {
                fetchItem('section', obj.id, copy);
            } else if (type === 'subsection') {
                if (angular.isUndefined(obj.subsections)) {
                    fetchItem('subsection', obj.id, copy);
                } else {
                    service.values.order = 0;
                }
            } else if (type === 'questionset') {
                fetchAttributeSets();
                if (angular.isDefined(obj.entities)) {
                    service.values.subsection = obj.id;
                    service.values.order = 0;
                } else {
                    fetchItem('questionset', obj.id, copy);
                }
            } else if (type === 'question') {
                fetchAttributes();
                if (angular.isDefined(obj.entities) ) {
                    // new question for a subsection
                    service.values.subsection = obj.id;
                    service.values.options = [];
                    service.values.order = 0;
                } else if (angular.isDefined(obj.questions) && obj.questions !== null) {
                    service.values.subsection = obj.subsection;
                    service.values.questionset = obj.id;
                    service.values.options = [];
                    service.values.order = 0;
                } else {
                    fetchItem('question', obj.id, copy);
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
