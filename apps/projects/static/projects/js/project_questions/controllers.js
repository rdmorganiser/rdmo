angular.module('project_questions')

.controller('QuestionsController', ['$scope', '$filter', 'QuestionsService', function($scope, $filter, QuestionsService) {

    $scope.service = QuestionsService;

    $scope.changeRadio = function(value, option_key) {
        if (angular.isDefined(value)) {
            value.key = option_key;
            if (angular.isUndefined(value.input)) {
                value.input = {};
            }
            value.text = value.input[option_key];
        }
    };

    $scope.checkCheckbox = function(event) {
        var checkbox = angular.element('input[type="checkbox"]', angular.element(event.target).parent())[0];
        if (checkbox.checked !== true) {
            checkbox.click();
        }
    };

    $scope.changeCheckbox = function(value, options) {
        if (angular.isDefined(value)) {
            var text = [];
            angular.forEach(value.checkbox, function(key) {
                var option = $filter('filter')(options, {'key': key})[0];

                if (option.input_field) {
                    if (angular.isUndefined(value.input)) {
                        value.input = {};
                    }
                    text.push(value.input[option.key]);
                } else {
                    text.push(option.text);
                }
            });

            value.key = JSON.stringify(value.checkbox);
            value.text = JSON.stringify(text);
        }
    };
}]);
