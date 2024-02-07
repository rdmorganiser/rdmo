angular.module('project_questions')

.controller('QuestionsController', ['$scope', '$filter', 'QuestionsService', function($scope, $filter, QuestionsService) {

    $scope.service = QuestionsService;

    $scope.checkCheckbox = function(event) {
        var checkbox = angular.element('input[type="checkbox"]', angular.element(event.target).parent().parent())[0];
        if (checkbox.checked !== true) {
            checkbox.click();
        }
    };
}]);
