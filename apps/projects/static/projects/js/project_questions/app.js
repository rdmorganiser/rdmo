angular.module('project_questions', ['formgroup', 'select-by-number', 'capitalize'])

// customizations for Django integration
.config(['$httpProvider', '$interpolateProvider', '$locationProvider', function($httpProvider, $interpolateProvider, $locationProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    // set the $location to not use #
    $locationProvider.html5Mode(true);
}]);
