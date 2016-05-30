angular.module('project_questions')

.directive('input', function() {
    return {
        restrict: 'E',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            if (attrs.type === 'checkbox') {
                ngModelController.$parsers.push(function(val) {
                    var values = [];
                    if (ngModelController.$modelValue) {
                        values = ngModelController.$modelValue;
                    }
                    var index = values.indexOf(attrs.key);

                    if (val === true && index === -1) {
                        values.push(attrs.key);
                    } else if (val === false && index !== -1) {
                        values.splice(index, 1);
                    }

                    return values.sort();
                });

                ngModelController.$formatters.push(function(val) {
                    if (angular.isDefined(val) && val.indexOf(attrs.key) !== -1) {
                        return true;
                    } else {
                        return false;
                    }
                });

                // workaround for non working ng-change
                scope.$watch(function(scope) {
                    if (angular.isDefined(ngModelController.$viewValue)) {
                        return ngModelController.$viewValue;
                    } else {
                        return false;
                    }
                }, function(newValue, oldValue) {
                    scope.$parent.$eval(attrs.change);
                });
            }
        }
    };
})

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
