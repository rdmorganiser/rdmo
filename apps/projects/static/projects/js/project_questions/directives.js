angular.module('project_questions')

.directive('input', ['$timeout', function($timeout) {
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
            } else if ($(element).hasClass('date')) {

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
        }
    };
}]);
