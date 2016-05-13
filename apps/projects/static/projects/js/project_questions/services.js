angular.module('project_questions')

.factory('QuestionsService', ['$http', '$timeout', '$location', '$filter', function($http, $timeout, $location, $filter) {

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'projects': baseurl + 'api/projects/projects/',
        'value_entities': baseurl + 'api/projects/entities/',
        'values': baseurl + 'api/projects/values/',
        'valuesets': baseurl + 'api/projects/valuesets/',
        'question_entities': baseurl + 'api/questions/entities/'
    };

    /* private methods */

    function valueFactory() {
        return {
            'text': ''
        };
    }

    function valueSetFactory() {
        var values = {};
        angular.forEach(service.questions, function(question, index) {
            values[question.attribute.id] = [valueFactory()];
        });

        return {
            'values': values,
        };
    }

    function initWidget(question, value) {
        value.input = {};

        if (question.widget_type === 'radio') {
            angular.forEach(question.options, function(option) {
                if (option.input_field) {
                    if (value.key === option.key) {
                        value.input[option.key] = value.text;
                    } else {
                        value.input[option.key] = '';
                    }
                }
            });
        }

        if (question.widget_type === 'checkbox') {
            if (value.key) {
                value.checkbox = JSON.parse(value.key);
                var text_array = JSON.parse(value.text);

                angular.forEach(question.options, function(option) {
                    if (option.input_field) {
                        var index = value.checkbox.indexOf(option.key);

                        if (index !== -1) {
                            value.input[option.key] = text_array[index];
                        } else {
                            value.input[option.key] = '';
                        }
                    }
                });
            } else {
                value.checkbox = [];
            }
        }
    }

    function fetchQuestionEntity(entity_id) {
        var url = urls.question_entities;
        if (entity_id) {
            url += entity_id + '/';
        } else {
            url += 'first/?catalog=' + service.project.catalog;
        }

        $http.get(url).success(function(response) {
            service.entity = response;

            if (service.entity.is_set) {
                service.questions = service.entity.questions;
            } else {
                service.questions = [service.entity];
            }

            $location.path('/' + service.entity.id + '/');

            fetchValueEntities();
        });
    }

    function fetchValueEntities() {

        service.values = {};

        var params = {
            snapshot: service.project.current_snapshot
        };
        if (service.entity.is_set) {
            params.valueset__attributeset = service.entity.attributeset.id;
        } else {
            params.value__attribute = service.entity.attribute.id;
        }

        $http.get(urls.value_entities, {'params': params}).success(function(response) {

            if (service.entity.is_set) {
                // store response from server or create new valuesets array
                if (response.length > 0) {
                    service.valuesets = response;

                    angular.forEach(service.valuesets, function(valueset, index) {
                        var values_array = valueset.values;

                        valueset.values = {};
                        angular.forEach(service.entity.questions, function(question, index) {
                            valueset.values[question.attribute.id] = [];
                        });

                        angular.forEach(values_array, function(value, index) {
                            if (angular.isDefined(valueset.values[value.attribute])) {
                                valueset.values[value.attribute].push(value);
                            } else if (value.attribute === service.entity.primary_attribute) {
                                valueset.values[value.attribute] = [value];
                            }
                        });

                        angular.forEach(service.entity.questions, function(question, index) {
                            if (valueset.values[question.attribute.id].length === 0) {
                                valueset.values[question.attribute.id].push(valueFactory());
                            }


                            angular.forEach(valueset.values[question.attribute.id], function(value) {
                                initWidget(question, value);
                            });
                        });
                    });

                } else {
                    service.valuesets = [valueSetFactory()];
                }

                service.values = service.valuesets[0].values;

            } else {
                // store response from server or create new values array
                if (response.length > 0) {
                    service.values[service.entity.attribute.id] = response;
                } else {
                    service.values[service.entity.attribute.id] = [valueFactory()];
                }

                angular.forEach(service.values[service.entity.attribute.id], function(value) {
                    initWidget(service.entity, value);
                });
            }

            $timeout(function() {
                $('.datepicker').datetimepicker({
                    format: 'YYYY-MM-DD'
                }).on('dp.change', function () {
                    $('.datepicker input').trigger('input');
                });
            });
        });
    }

    function storeValues(valueset) {
        if (angular.isDefined(valueset)) {
            values = valueset.values;
        } else {
            values = service.values;
        }

        angular.forEach(service.questions, function(question) {
            angular.forEach(values[question.attribute.id], function(value, index) {
                if (value.removed) {
                    // delete the value if it alredy exists on the server
                    if (angular.isDefined(value.id)) {
                        $http.delete(urls.values + value.id + '/');
                    }
                } else {
                    // store the current index in the list
                    value.index = index;
                    value.attribute = question.attribute.id;
                    value.snapshot = service.project.current_snapshot;

                    if (angular.isDefined(valueset)) {
                        value.valueset = valueset.id;
                    }

                    if (angular.isDefined(value.id)) {
                        // update an existing value
                        $http.put(urls.values + value.id + '/', value).success(function(response) {
                            angular.extend(value, response);
                        });
                    } else {
                        // update a new value
                        $http.post(urls.values, value).success(function(response) {
                            angular.extend(value, response);
                        });
                    }
                }
            });
        });
    }

    function storeValueSets() {
        angular.forEach(service.valuesets, function(valueset, index) {
            if (valueset.removed) {
                // delete the valueset
                if (angular.isDefined(valueset.id)) {
                    $http.delete(urls.valuesets + valueset.id + '/').success(function(response) {
                        // delete all the values or the valueset
                        angular.forEach(valueset.values, function(values) {
                            angular.forEach(values, function(value) {
                                $http.delete(urls.values + value.id + '/');
                            });
                        });
                    });
                }
            } else {
                // store the current index in the list
                valueset.index = index;
                valueset.attributeset = service.entity.attributeset.id;
                valueset.snapshot = service.project.current_snapshot;

                if (angular.isDefined(valueset.id)) {
                    // update an existing valueset
                    $http.put(urls.valuesets + valueset.id + '/', valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);

                        // // store values for this valueset
                        storeValues(valueset);
                    });
                } else {
                    // create a new valueset
                    $http.post(urls.valuesets, valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);

                        // // store values for this valueset
                        storeValues(valueset);
                    });
                }
            }
        });
    }

    function getValueSetIndex() {
        return $filter('filter')(service.valuesets, function(value, index, array) {
            return value.values == service.values;
        })[0].index;
    }

    function getPrevValueSet() {
        var i = getValueSetIndex();

        var prev_valueset = service.valuesets[i-1];
        if (angular.isDefined(prev_valueset) && !prev_valueset.removed) {
            return prev_valueset;
        } else {
            return false;
        }
    }

    function getNextValueSet() {
        var i = getValueSetIndex();

        var next_valueset = service.valuesets[i+1];
        if (angular.isDefined(next_valueset) && !next_valueset.removed) {
            return next_valueset;
        } else {
            return false;
        }
    }

    /* public methods */

    service.init = function(project_id) {
        $http.get(urls.projects + project_id + '/').success(function(response) {
            service.project = response;
            fetchQuestionEntity($location.path().replace(/\//g,''));
        });
    };

    service.prev = function() {
        if (service.entity.prev !== null) {
            fetchQuestionEntity(service.entity.prev);
        }
    };

    service.next = function() {
        if (service.entity.next !== null) {
            fetchQuestionEntity(service.entity.next);
        }
    };

    service.save = function(proceed) {
        if (service.entity.is_set) {
            storeValueSets();
        } else {
            storeValues();
        }

        if (angular.isDefined(proceed) && proceed) {
            if (service.entity.is_set) {
                var i = getValueSetIndex();
                if (angular.isDefined(service.valuesets[i + 1])) {
                    service.values = service.valuesets[i + 1].values;
                } else {
                    service.next();
                }
            } else {
                service.next();
            }
        }
    };

    service.addValue = function(attribute_id) {
        //  add new value to service.values
        if (angular.isUndefined(service.values[attribute_id])) {
            service.values[attribute_id] = [valueFactory()];
        } else {
            service.values[attribute_id].push(valueFactory());
        }
    };

    service.removeValue = function(attribute_id, index) {
        service.values[attribute_id][index].removed = true;
    };

    service.addValueSet = function() {
        // create a new valueset
        var valueset = valueSetFactory();

        // append the new valueset to the array of valuesets
        service.valuesets.push(valueset);

        // 'activate' the new valueset
        service.values = valueset.values;
    };


    service.removeValueSet = function() {
        // find current valueset
        var i = getValueSetIndex();

        // flag it for removal
        service.valuesets[i].removed = true;

        // activate the one before or after
        var prev_valueset = getPrevValueSet();
        if (prev_valueset) {
            service.values = prev_valueset.values;
        } else {
            var next_valueset = getNextValueSet();
            if (next_valueset) {
                service.values = next_valueset.values;
            } else {
                service.values = {};
            }

        }
    };

    return service;

}]);
