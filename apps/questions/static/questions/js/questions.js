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
            service.catalogId = response[0].id;
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

    function fetchEntities(subsection) {
        var url = entities_url + '?subsection=' + subsection.id;
        $http.get(entities_url).success(function(response) {
            subsection.entities = response;
        });
    }

    service.init = function() {
        fetchCatalogs();
    };

    service.changeCatalog = function() {
        fetchCatalog();
    };

    service.openModal = function(modal, action, entity) {
        console.log(modal, action, entity.id, entity.title);
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
