angular.module('project_questions')

.directive('rangeInput', ['$timeout', function($timeout) {
    return {
        restrict: 'C',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            if (attrs.minValue && attrs.maxValue) {
                ngModelController.$parsers.push(function(val) {
                    var min = parseFloat(attrs.minValue),
                        max = parseFloat(attrs.maxValue);

                    var value = 0.01 * (max - min) * (parseFloat(val) + min);
                    return Math.round(value / attrs.step) * attrs.step;
                });
                ngModelController.$formatters.push(function(val) {
                    var min = parseFloat(attrs.minValue),
                        max = parseFloat(attrs.maxValue);

                    return 100.0 / (max - min) * (parseFloat(val) + min);
                });
            }
        }
    };
}])

.directive('dateInput', ['$timeout', function($timeout) {
    return {
        restrict: 'C',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            ngModelController.$parsers.push(function(view_value) {

                if (view_value === '') {
                    return '';
                }

                if (attrs.language === 'de') {
                    return moment(view_value, 'DD.MM.YYYY').format();
                } else {
                    return moment(view_value).format();
                }

            });

            ngModelController.$formatters.push(function(model_value) {

                if (model_value === '') {
                    return '';
                }

                if (attrs.language === 'de') {
                    return moment(model_value).format('DD.MM.YYYY');
                } else {
                    return moment(model_value).format('MM/DD/YYYY');
                }

            });

            $timeout(function() {
                $('.date').datepicker({
                    autoclose: true,
                    clearBtn: true,
                    orientation: 'bottom',
                    language: attrs.language
                });
                $('.date:focus').datepicker('show');
            });
        }
    };
}]);
