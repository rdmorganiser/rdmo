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

    var catalogs_url = '/questions/api/catalogs/';

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
            });
    }

    service.init = function() {
        fetchCatalogs();
    };

    service.changeCatalog = function() {
        fetchCatalog();
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;
    $scope.service.init();

}]);
