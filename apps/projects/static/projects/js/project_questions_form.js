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

    function newValue() {
        return {'text': ''};
    }

    service = {
        options: {},
        values: [],
        errors: [],
        valueset: null
    };

    service.init = function(options) {
        service.options = options;
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

    service.addValue = function() {
        service.values.push(newValue());
    };

    service.removeValue = function(index) {
        service.values.splice(index, 1);
    };

    service.addValueSet = function() {
        service.valueset = {};

        angular.forEach(service.options.tags, function(tag) {
            service.valueset[tag] = [];
        });

        service.values.push(service.valueset);
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
            service.valueset[tag] = [newValue()];
        } else {
            service.valueset[tag].push(newValue());
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
