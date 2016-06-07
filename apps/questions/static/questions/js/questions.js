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

app.factory('QuestionsService', ['$http', '$timeout', '$window', '$q', function($http, $timeout, $window, $q) {

    var service = {};

    /* private variables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'catalogs': baseurl + 'api/questions/catalogs/',
        'sections': baseurl + 'api/questions/sections/',
        'subsections': baseurl + 'api/questions/subsections/',
        'question_entities': baseurl + 'api/questions/entities/',
        'questions': baseurl + 'api/questions/questions/',
        'questionsets': baseurl + 'api/questions/questionsets/',
        'widgettypes': baseurl + 'api/questions/widgettypes/',
        'attributes': baseurl + 'api/domain/attributes',
        'attribute_entitites': baseurl + 'api/domain/entities',
        'options': baseurl + 'api/domain/options/',
        'ranges': baseurl + 'api/domain/ranges/',
        'conditions': baseurl + 'api/domain/conditions/',
        'valuestypes': baseurl + 'api/domain/valuestypes/',
        'relations': baseurl + 'api/domain/relations/',
    };

    /* private methods */

    function factory() {

    }

    function fetchCatalog() {
        var config = {
            params: {
                nested: true
            }
        };

        return $http.get(urls.catalogs + service.current_catalog_id + '/', config)
            .success(function(response) {
                console.log(response);
                service.catalog = response;

                // service.sections = service.catalog.sections;
                // service.subsections = [];
                // service.questionsets = [];

                // angular.forEach(service.sections, function(section) {
                //     angular.forEach(section.subsections, function(subsection) {
                //         service.subsections.push({
                //             id: subsection.id,
                //             title: subsection.title
                //         });

                //         angular.forEach(subsection.entities, function(entity) {
                //             if (entity.is_set) {
                //                 service.questionsets.push({
                //                     id: entity.id,
                //                     title: entity.title
                //                 });
                //             }
                //         });
                //     });
                // });
            });
    }

    function fetchItem(ressource, id, copy) {
        $http.get(urls[ressource] + id + '/')
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

    function storeItem(ressource, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        if (angular.isUndefined(values.id)) {
            $http.post(urls[ressource], values)
                .success(function(response) {
                    if (ressource === 'catalogs') {
                        service.catalogId = response.id;
                        fetchCatalogs();
                    } else if (ressource === 'questionsets') {
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('conditions', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('conditions', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (ressource === 'questions') {
                        angular.forEach(values.options, function(option) {
                            if (option.removed === true) {
                                deleteItem('options', option);
                            } else {
                                option.question = response.id;
                                if (angular.isUndefined(option.input_field)) {
                                    option.input_field = false;
                                }
                                storeItem('options', option);
                            }
                        });
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('conditions', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('conditions', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (ressources === 'options' || ressources === 'conditions') {
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
            $http.put(urls[ressource] + values.id + '/', values)
                .success(function(response) {
                    if (ressource === 'catalogs') {
                        service.catalogId = response.id;
                        fetchCatalogs();
                    } else if (ressource === 'questionsets') {
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('conditions', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('conditions', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (ressource === 'questions') {
                        angular.forEach(values.options, function(option) {
                            if (option.removed === true) {
                                deleteItem('options', option);
                            } else {
                                option.question = response.id;
                                if (angular.isUndefined(option.input_field)) {
                                    option.input_field = false;
                                }
                                storeItem('options', option);
                            }
                        });
                        angular.forEach(values.conditions, function(condition) {
                            if (condition.removed === true) {
                                deleteItem('conditions', condition);
                            } else {
                                condition.question_entity = response.id;
                                storeItem('conditions', condition);
                            }
                        });
                        fetchCatalog();
                    } else if (ressource === 'options' || ressource === 'conditions') {
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

    function deleteItem(ressource, values) {
        if (angular.isUndefined(values)) {
            values = service.values;
        }

        $http.delete(urls[ressource] + values.id + '/')
            .success(function(response) {
                if (ressource === 'catalogs') {
                    delete service.catalogId;
                    delete service.catalog;
                    fetchCatalogs();
                } else if (ressource === 'options') {
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

        var p1 = $http.get(urls.attributes).success(function(response) {
            service.attributes = response;
        });
        var p2 = $http.get(urls.widgettypes).success(function(response) {
            service.widgettypes = response;
        });
        var p3 = $http.get(urls.catalogs).success(function(response) {
            service.catalogs = response;
            service.current_catalog_id = service.catalogs[0].id;

            fetchCatalog().success(function() {
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

        return $q.all([p1, p2, p3]);
    };

    service.changeCatalog = function() {
        fetchCatalog();
    };

    service.openFormModal = function(ressource, obj, copy) {

        service.errors = {};
        service.values = {};

        if (angular.isDefined(obj)) {
            if (ressource === 'catalogs') {
                service.values = angular.copy(obj);
            } else if (ressource === 'sections') {
                fetchItem('section', obj.id, copy);
            } else if (ressource === 'subsections') {
                if (angular.isUndefined(obj.subsections)) {
                    fetchItem('subsections', obj.id, copy);
                } else {
                    service.values.order = 0;
                }
            } else if (ressource === 'questionsets') {
                fetchAttributeSets();
                if (angular.isDefined(obj.entities)) {
                    service.values.subsection = obj.id;
                    service.values.order = 0;
                } else {
                    fetchItem('questionsets', obj.id, copy);
                }
            } else if (ressource === 'questions') {
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
                    fetchItem('questions', obj.id, copy);
                }
            }
        } else {
            if (ressource === 'catalogs') {
                // nothing to do, move along
            } else if (ressource === 'sections') {
                service.values.order = 0;
                service.values.catalog = service.catalog.id;
            } else if (ressource === 'subsections') {
                service.values.order = 0;
            } else if (ressource === 'questionsets') {
                fetchAttributeSets();
                service.values.order = 0;
            } else if (ressource === 'questions') {
                fetchAttributes();
                service.values.order = 0;
            }
        }

        $timeout(function() {
            $('#' + ressource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(ressource) {
        storeItem(ressource);
    };

    service.openDeleteModal = function(ressource, obj) {
        service.values = obj;
        $('#' + ressource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(ressource) {
        deleteItem(ressource);
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
