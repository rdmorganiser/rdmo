angular.module('project_questions', ['core'])

.config(['$locationProvider', function($locationProvider) {

    // set $location to not use #
    $locationProvider.html5Mode(true);

}]);
