var app = angular.module('project_questions', ['form-fields']);

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

    var base = angular.element('base').attr('href');

    var urls = {
        'projects': base + '/projects/api/projects/',
        'values': base + '/projects/api/values/',
        'valuesets': base + '/projects/api/valuesets/',
        'question_entities': base + '/questions/api/entities/'
    };

    service = {
        options: {},
        project: {}
    };

    function fetchProject() {
        $http.get(urls.projects + service.project_id + '/').success(function(response) {
            service.project = response;
        });
    }

    function fetchQuestionEntity() {
        $http.get(urls.question_entities + service.entity_id + '/').success(function(response) {
            service.entity = response;
        });
    }

    service.init = function(project_id, entity_id) {
        service.project_id = project_id;
        service.entity_id = entity_id;

        fetchProject();
        fetchQuestionEntity();
    };

    service.location = function(mode) {
        $http.get(urls.question_entities + service.entity_id + '/' + mode).success(function(response) {
            service.entity_id = response.id;
            fetchQuestionEntity();
        });
    };

    return service;

}]);

app.controller('QuestionsController', ['$scope', 'QuestionsService', function($scope, QuestionsService) {

    $scope.service = QuestionsService;

}]);
