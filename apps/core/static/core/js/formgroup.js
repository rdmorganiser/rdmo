angular.module('formgroup', [])

.directive('formgroup', function() {

    return {
        scope: {
            id: '@',
            label: '@',
            model: '=',
            errors: '=',
            options: '=',
            optionsLabel: '@',
            'null': '@',

        },
        templateUrl: function(element, attrs) {
            var staticurl = angular.element('meta[name="staticurl"]').attr('content');
            return staticurl + 'core/html/formgroup_' + attrs.type + '.html';
        }
    };
});
