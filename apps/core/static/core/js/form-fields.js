angular.module('form-fields', [])

.directive('textfield', function() {
    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: angular.element('base').attr('href') + '/static/core/html/textfield.html'
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
        templateUrl: angular.element('base').attr('href') + '/static/core/html/textareafield.html'
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
        templateUrl: angular.element('base').attr('href') + '/static/core/html/checkboxfield.html'
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
        templateUrl: angular.element('base').attr('href') + '/static/core/html/numberfield.html'
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
        templateUrl: angular.element('base').attr('href') + '/static/core/html/selectfield.html'
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
        templateUrl: angular.element('base').attr('href') + '/static/core/html/selectnumberfield.html'
    };
});