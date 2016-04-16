var app = angular.module('questions', ['select-by-number']);

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

    var catalogs_url = '/questions/api/catalogs/',
        entities_url = '/questions/api/entities/',
        questions_url = '/questions/api/questions/',
        questionsets_url = '/questions/api/questionsets/';

    service = {
        values: {},
        errors: {},
        catalogs: []
    };

    function fetchCatalogs() {
        $http.get(catalogs_url).success(function(response) {
            service.catalogs = response;

            if (angular.isUndefined(service.catalogId)) {
                service.catalogId = response[0].id;
            }

            fetchCatalog();
        });
    }

    function fetchCatalog() {
        var url = catalogs_url + service.catalogId + '/';
        $http.get(url)
            .success(function(response) {
                service.catalog = response;

                angular.forEach(service.catalog.sections, function(section) {
                    angular.forEach(section.subsections, function(subsection) {
                        fetchEntities(subsection);
                    });
                });
            });
    }

    function createCatalog() {
        $http.post(catalogs_url, service.values)
            .success(function(response) {
                service.catalogId = response.id;
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function updateCatalog() {
        $http.put(catalogs_url + service.values.id + '/', service.values)
            .success(function(response) {
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function deleteCatalog() {
        $http.delete(catalogs_url + service.values.id + '/', service.values)
            .success(function(response) {
                delete service.catalogId;
                fetchCatalogs();
                $('.modal').modal('hide');
            })
            .error(function(response, status) {
                service.errors = response;
            });
    }

    function fetchEntities(subsection) {
        var url = entities_url + '?subsection=' + subsection.id;
        $http.get(url).success(function(response) {
            subsection.entities = response;
        });
    }

    service.init = function() {
        fetchCatalogs();
    };

    service.changeCatalog = function() {
        fetchCatalog();
    };

    service.openCatalogFormModal = function(entity) {
        if (angular.isDefined(entity)) {
            service.values = angular.copy(service.catalog);
        } else {
            service.values = {};
        }

        service.errors = {};

        $timeout(function() {
            $('#catalog-form-modal').modal('show');
        });
    };

    service.submitCatalogFormModal = function() {
        if (angular.isUndefined(service.values.id)) {
            createCatalog();
        } else {
            updateCatalog();
        }
    };

    service.openCatalogDeleteModal = function(entity) {
        $('#catalog-delete-modal').modal('show');
    };

    service.submitCatalogDeleteModal = function() {
        $('.modal').modal('hide');
    };
    

    service.openSectionFormModal = function(entity) {
        $('#section-form-modal').modal('show');
    };

    service.openSubsectionFormModal = function(entity) {
        $('#subsection-form-modal').modal('show');
    };

    service.openQuestionFormModal = function(entity) {
        $('#question-form-modal').modal('show');
    };

    service.openQuestionSetFormModal = function(entity) {
        $('#questionset-form-modal').modal('show');
    };



    service.submitSectionFormModal = function() {
        $('.modal').modal('hide');
    };

    service.submitSubsectionFormModal = function() {
        $('.modal').modal('hide');
    };

    service.submitQuestionFormModal = function() {
        $('.modal').modal('hide');
    };

    service.submitQuestionSetFormModal = function() {
        $('.modal').modal('hide');
    };





    service.openSectionDeleteModal = function(entity) {
        $('#section-delete-modal').modal('show');
    };

    service.openSubsectionDeleteModal = function(entity) {
        $('#subsection-delete-modal').modal('show');
    };

    service.openQuestionDeleteModal = function(entity) {
        $('#question-delete-modal').modal('show');
    };

    service.openQuestionSetDeleteModal = function(entity) {
        $('#questionset-delete-modal').modal('show');
    };





    service.submitSectionDeleteModal = function() {
        $('.modal').modal('hide');
    };

    service.submitSubsectionDeleteModal = function() {
        $('.modal').modal('hide');
    };

    service.submitQuestionDeleteModal = function() {
        $('.modal').modal('hide');
    };

    service.submitQuestionSetDeleteModal = function() {
        $('.modal').modal('hide');
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
