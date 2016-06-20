angular.module('capitalize', [])

.filter('capitalize', function() {
    return function(input, scope) {
        if (angular.isDefined(input)) {
            return input.substring(0,1).toUpperCase()+input.substring(1);
        } else {
            return '';
        }
    };
});
