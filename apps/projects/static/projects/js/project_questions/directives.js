angular.module('project_questions')

.directive('input', function() {
    return {
        restrict: 'E',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            if (attrs.type === 'range') {
                if (attrs.minValue && attrs.maxValue) {
                    ngModelController.$parsers.push(function(val) {
                        var min = parseFloat(attrs.minValue),
                            max = parseFloat(attrs.maxValue);

                        return 0.01 * (max - min) * (parseFloat(val) + min);
                    });
                    ngModelController.$formatters.push(function(val) {
                        var min = parseFloat(attrs.minValue),
                            max = parseFloat(attrs.maxValue);

                        return 100.0 / (max - min) * (parseFloat(val) + min);
                    });
                }
            }
        }
    };
});
