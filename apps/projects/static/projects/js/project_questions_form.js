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

    var values_url = '/projects/api/values/',
        valuesets_url = '/projects/api/valuesets/';

    function newValue(attribute_id, valueset_id) {
        var value = {
            'text': '',
            'snapshot': service.options.snapshot.id,
            'attribute': service.options.attribute.id
        };

        if (angular.isDefined(attribute_id)) {
            value['attribute'] = attribute_id;
        }

        if (angular.isDefined(valueset_id)) {
            value['valueset'] = valueset_id;
        }

        return value;
    }

    function newValueSet() {
        return {
            'values': {},
            'snapshot': service.options.snapshot.id,
            'attributeset': service.options.attributeset.id
        };
    }

    service = {
        options: {},
        values: [],
        valuesets: [],
        active_valueset: null,
        errors: {}
    };

    service.init = function(options) {
        // store options from the Django template
        service.options = options;

        // call fetch functions for valuesets or values
        if (service.options.attributeset) {
            service.fetchValueSets();
        } else {
            service.fetchValues();
        }
    };

    service.save = function() {
        //  call store functions for valuesets or values
        if (service.options.attributeset) {
            service.storeValueSets();
        } else {
            service.storeValues();
        }
    };

    service.redirect = function(url) {
        window.location = url;
    };

    service.saveAndRedirect = function(url) {
        service.save();
        //service.redirect(url);
    };

    service.fetchValues = function() {
        $http.get(values_url, {
            params: {
                attribute: service.options.attribute.id
            }
        }).success(function(response) {
            // store response from server or create new values array
            if (response.length > 0) {
                service.values = response;
            } else {
                service.values = [newValue()];
            }
        });
    };

    service.storeValues = function() {
        angular.forEach(service.values, function(value, index) {
            if (value.removed) {
                // delete the value if it alredy exists on the server
                if (angular.isDefined(value.id)) {
                    $http.delete(values_url + value.id);
                }
            } else {
                // store the current index in the list
                value.index = index;

                if (angular.isDefined(value.id)) {
                    // update an existing value
                    $http.put(values_url + value.id, value).success(function(response) {
                        service.values[index] = response;
                    });
                } else {
                    // update a new value
                    $http.post(values_url, value).success(function(response) {
                        service.values[index] = response;
                    });
                }
            }
        });
    };

    service.addValue = function() {
        if (angular.isUndefined(service.values)) {
            service.values = [newValue()];
        } else {
            service.values.push(newValue());
        }
    };

    service.removeValue = function(index) {
        service.values[index].removed = true;
    };

    service.fetchValueSets = function() {
        // fetch the valuesets from the server
        $http.get(valuesets_url, {
            params: {
                attributeset: service.options.attributeset.id
            }
        }).success(function(response) {
            // store response from server or create new valuesets array
            if (response.length > 0) {
                service.valuesets = response;
            } else {
                service.valuesets = [newValueSet()];
            }

            angular.forEach(service.valuesets, function(valueset, index) {
                // create an empty values object
                valueset.values = {};

                angular.forEach(service.options.attributeset.attributes, function(attribute) {
                    valueset.values[attribute.id] = [];
                });

                if (angular.isDefined(valueset.id)) {
                    // fetch the values for this valueset from the server
                    $http.get(values_url, {
                        params: {
                            valueset: valueset.id
                        }
                    }).success(function(response) {
                        angular.forEach(response, function(value) {
                            valueset.values[value.attribute].push(value);
                        });

                        angular.forEach(service.options.attributeset.attributes, function(attribute) {
                            if (valueset.values[attribute.id].length === 0) {
                                valueset.values[attribute.id].push(newValue(attribute.id, valueset.id));
                            }
                        });
                    });
                } else {
                    angular.forEach(service.options.attributeset.attributes, function(attribute) {
                        valueset.values[attribute.id].push(newValue(attribute.id, valueset.id));
                    });
                }
            });

            service.valueset = service.valuesets[0];
        });
    };

    service.storeValueSets = function() {
        angular.forEach(service.valuesets, function(valueset, index) {
            if (valueset.removed) {
                // delete the valueset
                if (angular.isDefined(valueset.id)) {
                    $http.delete(valuesets_url + valueset.id).success(function(response) {
                        // delete all the values or the valueset
                        angular.forEach(valueset.values, function(values) {
                            angular.forEach(values, function(value) {
                                $http.delete(values_url + value.id);
                            });
                        });
                    });
                }
            } else {
                // store the current index in the list
                valueset.index = index;

                if (angular.isDefined(valueset.id)) {
                    // update an existing valueset
                    $http.put(valuesets_url + valueset.id, valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);

                        // store values for this valueset
                        service.storeValueSetValues(valueset);
                    });
                } else {
                    // create a new valueset
                    $http.post(valuesets_url, valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);

                        // store values for this valueset
                        service.storeValueSetValues(valueset);
                    });
                }
            }
        });
    };

    service.storeValueSetValues = function(valueset) {

        // loop over all arrays of values in the valueset
        angular.forEach(valueset.values, function(values, attribute_id) {
            // loop over all values in the array
            angular.forEach(values, function(value, index) {
                if (value.removed) {
                    // delete the value if it alredy exists on the server
                    if (angular.isDefined(value.id)) {
                        $http.delete(values_url + value.id);
                    }
                } else {
                    // store the current index in the list
                    value.index = index;

                    // add the valueset id to the value if it was not set before (new valueset)
                    if (angular.isUndefined(value.valueset)) {
                        value.valueset = valueset.id;
                    }

                    if (angular.isDefined(value.id)) {
                        // update an existing value
                        $http.put(values_url + value.id, value).success(function(response) {
                            valueset.values[attribute_id][index] = response;
                        });
                    } else {
                        // create a new value
                        $http.post(values_url, value).success(function(response) {
                            valueset.values[attribute_id][index] = response;
                        });
                    }
                }
            });
        });
    };

    service.addValueSet = function() {
        // create a new valueset locally, already active
        service.valueset = newValueSet();

        // loop over attributes and create values for the valueset
        angular.forEach(service.options.attributeset.attributes, function(attribute) {
            service.valueset.values[attribute.id]= [newValue(attribute.id, service.valueset.id)];
        });

        // append the new valueset to the array of valuesets
        service.valuesets.push(service.valueset);
    };

    service.removeValueSet = function() {
        // flag the valueset as removed
        service.valueset.removed = true;

        // activate previous valueset or the next one
        var index = service.valuesets.indexOf(service.valueset);
        if (index > 0) {
            service.valueset = service.valuesets[index - 1];
        } else {
            service.valueset = service.valuesets[index];
        }
    };

    service.addValueSetValue = function(attribute_id) {
        // add new value with a given attribute_id to the current valueset
        if (angular.isUndefined(service.valueset.values[attribute_id])) {
            service.valueset.values[attribute_id] = [newValue(attribute_id, service.valueset.id)];
        } else {
            service.valueset.values[attribute_id].push(newValue(attribute_id, service.valueset.id));
        }
    };

    service.removeValueSetValue = function(attribute_id, index) {
        // flag the value as removed
        service.valueset.values[attribute_id][index].removed = true;
    };

    return service;

}]);

app.controller('FormController', ['$scope', 'FormService', function($scope, FormService) {

    $scope.service = FormService;

}]);
