var app = angular.module('project_questions_form', []);

// customizations for Django integration
app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    // use {$ and $} as tags for angular
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    // set Django's CSRF Cookie and Header
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('FormService', ['$http', '$timeout', function($http, $timeout) {

    service = {
        options: {},
        values: {},
        errors: {}
    };

    service.init = function(options) {
        service.options = options;

        if (service.options.attributeset) {
            service.initValueSets();
        } else {
            service.initValues();
        }
    };

    service.prev = function() {
        console.log('prev');
    };

    service.next = function() {
        console.log('next');
    };

    service.save = function() {
        console.log('save');
        console.log(service.values);
    };

    service.saveAndNext = function() {
        console.log('saveAndNext');
        console.log(service.values);
    };

    service.initValues = function() {
        if (service.options.attribute.is_collection) {
            service.values[service.options.attribute.tag] = [''];
        } else {
            service.values[service.options.attribute.tag] = '';
        }
    };

    service.addValue = function(tag) {
        if (angular.isUndefined(service.values)) {
            service.values = {};
        }

        if (angular.isUndefined(service.values[tag])) {
            service.values[tag] = [''];
        } else {
            service.values[tag].push('');
        }
    };

    service.removeValue = function(tag, index) {
        service.values[tag].splice(index, 1);
    };

    service.initValueSets = function() {
        service.valueset = {};
        service.initValueSetValues();

        if (service.options.attributeset.is_collection) {
            service.values[service.options.attributeset.tag] = [service.valueset];
        } else {
            service.values[service.options.attributeset.tag] = service.valueset;
        }
    };

    service.initValueSetValues = function() {
        angular.forEach(service.options.attributeset.attributes, function(attribute) {
            if (attribute.is_collection) {
                service.valueset[attribute.tag] = [''];
            } else {
                service.valueset[attribute.tag] = '';
            }
        });
    };

    service.addValueSet = function() {
        service.valueset = {};
        service.values[service.options.attributeset.tag].push(service.valueset);
        service.initValueSetValues();
    };

    service.removeValueSet = function() {
        var index = service.values.indexOf(service.valueset);
        service.values.splice(index, 1);

        if (index > 0) {
            service.valueset = service.values[index - 1];
        } else {
            service.valueset = service.values[index];
        }
    };

    service.addValueSetValue = function(tag) {
        if (angular.isUndefined(service.valueset[tag])) {
            service.valueset[tag] = [''];
        } else {
            service.valueset[tag].push('');
        }
    };

    service.removeValueSetValue = function(tag, index) {
        service.valueset[tag].splice(index, 1);
    };

    return service;

}]);

app.controller('FormController', ['$scope', 'FormService', function($scope, FormService) {

    $scope.service = FormService;

}]);
