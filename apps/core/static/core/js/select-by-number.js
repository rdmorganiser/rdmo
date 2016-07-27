angular.module('select-by-number', [])

.directive('byNumber', function() {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {

            if (attrs.multiple) {

                ngModel.$parsers.push(function(view_values) {
                    if (angular.isArray(view_values)) {
                        model_values = view_values.map(function (view_value) {
                            return parseInt(view_value, 10);
                        });
                        return model_values;
                    } else {
                        return view_values;
                    }
                });

                ngModel.$formatters.push(function(model_values) {
                    if (angular.isArray(model_values)) {
                        view_values = model_values.map(function (model_value) {
                            return '' + model_value;
                        });
                        console.log(view_values);

                        return view_values;
                    } else {
                        return model_values;
                    }
                });

            } else {

                ngModel.$parsers.push(function(view_value) {
                    if (view_value === 'null') {
                        return null;
                    } else {
                        return parseInt(view_value, 10);
                    }
                });

                ngModel.$formatters.push(function(model_value) {
                    if (model_value === null) {
                        return 'null';
                    } else {
                        return '' + model_value;
                    }
                });

            }
        }
    };
});
