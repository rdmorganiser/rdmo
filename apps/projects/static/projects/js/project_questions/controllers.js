angular.module('project_questions')

.controller('QuestionsController', ['$scope', '$filter', 'QuestionsService', function($scope, $filter, QuestionsService) {

    $scope.service = QuestionsService;

    $scope.changeRadio = function(value, option_id) {
        if (angular.isDefined(value)) {
            value.option = option_id;
            if (angular.isUndefined(value.input)) {
                value.input = {};
            }
            console.log(value.input[option_id]);
            value.text = value.input[option_id];
        }
    };

    $scope.checkCheckbox = function(event) {
        var checkbox = angular.element('input[type="checkbox"]', angular.element(event.target).parent())[0];
        if (checkbox.checked !== true) {
            checkbox.click();
        }
    };
}]);
