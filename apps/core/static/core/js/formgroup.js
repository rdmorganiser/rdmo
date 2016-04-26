angular.module('formgroup', [])

.directive('formgroup', function() {

    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '='
        },
        templateUrl: function (element, attrs) {
            return angular.element('base').attr('href') + '/static/core/html/formgroup_' + attrs.type + '.html';
        }
    };
});
