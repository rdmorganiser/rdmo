angular.module('project_questions')

.controller('QuestionsController', ['$scope', '$filter', 'QuestionsService', function($scope, $filter, QuestionsService) {

    $scope.service = QuestionsService;

    $scope.changeRadio = function(value, index) {
        if (angular.isDefined(value)) {
            value.selected = index;
            if (angular.isUndefined(value.additional_input)) {
                value.additional_input = {};
            }

            value.text = value.additional_input[index];
        }
    };

    $scope.checkCheckbox = function(event) {
        var checkbox = angular.element('input[type="checkbox"]', angular.element(event.target).parent())[0];
        if (checkbox.checked !== true) {
            checkbox.click();
        }
    };
}]);
