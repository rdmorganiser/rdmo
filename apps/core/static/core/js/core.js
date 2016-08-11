angular.module('core', ['ngResource'])

.config(['$httpProvider', '$interpolateProvider', '$resourceProvider', function($httpProvider, $interpolateProvider,$resourceProvider) {

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set $reosurce not to strip slashes and add an update action
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $resourceProvider.defaults.actions.update = {
        method: 'PUT',
        params: {}
    };
}])

.filter('capitalize', function() {
    return function(input, scope) {
        if (angular.isDefined(input)) {
            return input.substring(0,1).toUpperCase()+input.substring(1);
        } else {
            return '';
        }
    };
})

.directive('formgroup', function() {

    return {
        scope: {
            id: '@',
            label: '@',
            help: '@',
            model: '=',
            errors: '=',
            options: '=',
            optionsLabel: '@',
            optionsFilter: '=',
            optionsNull: '@',
            rows: '@?'
        },
        templateUrl: function(element, attrs) {
            var staticurl = angular.element('meta[name="staticurl"]').attr('content');
            return staticurl + 'core/html/formgroup_' + attrs.type + '.html';
        },
        controller: function($scope) {
            $scope.rows = angular.isDefined($scope.rows) ? $scope.rows : 4;
        }
    };
})

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
