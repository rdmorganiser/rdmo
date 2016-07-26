var app = angular.module('conditions', ['core', 'select-by-number', 'formgroup']);

app.factory('ConditionsService', ['$http', '$timeout', '$window', '$q', 'ResourcesService', function($http, $timeout, $window, $q, ResourcesService) {

    /* get the base url */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    /* create the domain service */

    var service = {};

    /* create and configure the resource service */

    var resources = ResourcesService;

    resources.urls = {
        'conditions': baseurl + 'api/conditions/conditions/',
        'attributes': baseurl + 'api/conditions/attributes/',
        'relations': baseurl + 'api/conditions/relations/'
    };

    resources.service = service;

    resources.factory = function(resource, parent) {
        if (resource === 'conditions') {
            return {
                'source': null,
                'relation': null,
                'target_option': null
            };
        }
    };

    /* configure the domain service */

    service.init = function(options) {
        resources.fetchItems('attributes');
        resources.fetchItems('relations').then(function(result) {
            service.relations_dict = result.data.reduce(function (previousValue, currentValue, currentIndex, array) {
                previousValue[currentValue.id] = currentValue.text;
                return previousValue;
            }, {});
        });

        service.initConditions();

        $window.addEventListener('beforeunload', function() {
            sessionStorage.setItem('current_scroll_pos', $window.scrollY);
        });
    };

    service.initConditions = function(options) {
        return $http.get(resources.urls['conditions'] + 'index/').success(function(response) {
            service.conditions = response;
        });
    };

    service.openFormModal = function(resource, obj, create) {
        service.errors = {};
        service.values = {};

        if (angular.isDefined(create) && create) {
            service.values = resources.factory(resource, obj);
        } else {
            resources.fetchItem(resource, obj.id);
        }

        $timeout(function() {
            $('#' + resource + '-form-modal').modal('show');
        });
    };

    service.submitFormModal = function(resource) {
        resources.storeItem(resource).then(function() {
            $('#' + resource + '-form-modal').modal('hide');
            service.initConditions();
        });
    };

    service.openDeleteModal = function(resource, obj) {
        service.values = obj;
        $('#' + resource + '-delete-modal').modal('show');
    };

    service.submitDeleteModal = function(resource) {
        resources.deleteItem(resource).then(function() {
            $('#' + resource + '-delete-modal').modal('hide');
            service.initConditions();
        });
    };

    return service;

}]);

app.controller('ConditionsController', ['$scope', 'ConditionsService', function($scope, ConditionsService) {

    $scope.service = ConditionsService;
    $scope.service.init();

}]);
