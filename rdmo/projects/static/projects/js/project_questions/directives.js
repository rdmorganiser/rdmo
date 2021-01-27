angular.module('project_questions')

.directive('rangeInput', ['$timeout', function($timeout) {
    return {
        restrict: 'C',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {

            /* (val / 100.0) = (range_val - min) / (max - min) */

            if (attrs.minValue && attrs.maxValue) {
                ngModelController.$parsers.push(function(val) {
                    var min = parseFloat(attrs.minValue),
                        max = parseFloat(attrs.maxValue);

                    var value = 0.01 * parseFloat(val) * (max - min) + min;
                    var d = 100 * attrs.step;
                    return Math.round(value * d) / d;
                });

                ngModelController.$formatters.push(function(val) {
                    var min = parseFloat(attrs.minValue),
                        max = parseFloat(attrs.maxValue);

                    var value = 100.0 * (parseFloat(val) - min) / (max - min);
                    return value;
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

            var lang = 'en',
                datepicker_format = 'yyyy-mm-dd',
                moment_format = 'YYYY-MM-DD';

            if (attrs.language === 'de') {
                lang = 'de';
                datepicker_format = 'dd.mm.yyyy';
                moment_format = 'DD.MM.YYYY';
            }

            ngModelController.$parsers.push(function(view_value) {
                if (view_value === '') {
                    return view_value;
                } else {
                    return moment(view_value, moment_format).format();
                }
            });

            ngModelController.$formatters.push(function(model_value) {
                if (model_value === '') {
                    return '';
                } else {
                    return moment(model_value).format(moment_format);
                }
            });

            $timeout(function() {
                $('.date').datepicker({
                    autoclose: true,
                    clearBtn: true,
                    orientation: 'bottom',
                    language: attrs.language,
                    format: datepicker_format,
                    weekStart: 1
                });
                $('.date:focus').datepicker('show');
            });
        }
    };
}])

.directive('fileInput', ['$timeout', function($timeout) {
    return {
        restrict: 'C',
        scope: true,
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            element.on('change', function() {
                scope.$evalAsync(read);
            });
            read();

            function read() {
                var file = element[0].files[0];
                ngModelController.$setViewValue(file);
            }

            ngModelController.$formatters.push(function(model_value) {
                if (model_value === false) {
                    // reset input["file"] field if model was set to false
                    angular.element(element).val(null);
                }
                return model_value;
            });
        }
    };
}]);
