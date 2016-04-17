angular.module('form-fields', [])

.directive('textfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: '/static/core/html/textfield.html'
    };
})

.directive('textareafield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: '/static/core/html/textareafield.html'
    };
})

.directive('checkboxfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: '/static/core/html/checkboxfield.html'
    };
})

.directive('numberfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: '/static/core/html/numberfield.html'
    };
})

.directive('selectfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '=',
            options: '=',
            text: '@',
            'null': '@'
        },
        templateUrl: '/static/core/html/selectfield.html'
    };
})

.directive('selectnumberfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '=',
            options: '=',
            text: '@',
            'null': '@'
        },
        templateUrl: '/static/core/html/selectnumberfield.html'
    };
});