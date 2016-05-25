angular.module('project_questions')

.factory('QuestionsService', ['$http', '$timeout', '$location', '$filter', '$q', '$window', function($http, $timeout, $location, $filter, $q, $window) {

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'projects': baseurl + 'api/projects/projects/',
        'value_entities': baseurl + 'api/projects/entities/',
        'values': baseurl + 'api/projects/values/',
        'valuesets': baseurl + 'api/projects/valuesets/',
        'catalog': baseurl + 'api/questions/catalogs/',
        'question_entities': baseurl + 'api/questions/entities/'
    };

    var back = false;

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

        if (question.widget_type === 'range') {
            if (!value.text) {
                value.text = '0';
            }
        }
    }

    function checkCondition(condition, value_entity) {
        if (condition.relation === 'eq') {
            if (value_entity.key && value_entity.key == condition.value) {
                return true;
            } else if (value_entity.text == condition.value) {
                return true;
            } else {
                return false;
            }
        } else if (condition.relation === 'neq') {
            if (value_entity.key && value_entity.key == condition.value) {
                return false;
            } else if (value_entity.text == condition.value) {
                return false;
            } else {
                return true;
            }
        }
    }

    function fetchCatalog() {
        return $http.get(urls.catalog + service.project.catalog + '/')
            .success(function(response) {
                service.catalog = response;
            });
    }

    function fetchQuestionEntity(entity_id) {
        var url = urls.question_entities;
        if (entity_id) {
            url += entity_id + '/';
        } else {
            url += 'first/?catalog=' + service.project.catalog;
        }

        $http.get(url).success(function(response) {

            var promises = [];
            angular.forEach(response.conditions, function (condition) {
                var params = {
                    snapshot: service.project.current_snapshot,
                    value__attribute: condition.attribute
                };

                promises.push($http.get(urls.value_entities, {'params': params}));
            });

            $q.all(promises).then(function(results) {
                var checks = [];
                var value_entities = {};

                angular.forEach(results, function (result) {
                    value_entities[result.config.params.value__attribute] = result.data;
                });

                angular.forEach(response.conditions, function (condition) {
                    angular.forEach(value_entities[condition.attribute], function (value_entity) {
                        checks.push(checkCondition(condition, value_entity));
                    });
                });

                if (checks.length && checks.indexOf(true) === -1) {
                    if (back) {
                        fetchQuestionEntity(response.prev);
                    } else {
                        fetchQuestionEntity(response.next);
                    }
                } else {
                    service.entity = response;

                    if (service.entity.is_set) {
                        service.questions = service.entity.questions;
                    } else {
                        service.questions = [service.entity];
                    }

                    $location.path('/' + service.entity.id + '/');

                    back = false;

                    $window.scrollTo(0, 0);

                    fetchValueEntities();
                }
            });
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

        var promises = [];

        angular.forEach(service.questions, function(question) {
            angular.forEach(values[question.attribute.id], function(value, index) {
                var promise;

                if (value.removed) {
                    // delete the value if it alredy exists on the server
                    if (angular.isDefined(value.id)) {
                        promise = $http.delete(urls.values + value.id + '/');
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
                        promise = $http.put(urls.values + value.id + '/', value).success(function(response) {
                            angular.extend(value, response);
                        });
                    } else {
                        // update a new value
                        promise = $http.post(urls.values, value).success(function(response) {
                            angular.extend(value, response);
                        });
                    }
                }

                promises.push(promise);
            });
        });

        return $q.all(promises);
    }

    function storeValueSets() {
        var promises = [];

        angular.forEach(service.valuesets, function(valueset, index) {
            var promise;

            if (valueset.removed) {
                // delete the valueset
                if (angular.isDefined(valueset.id)) {
                    promise = $http.delete(urls.valuesets + valueset.id + '/').success(function(response) {
                        // delete all the values or the valueset
                        angular.forEach(valueset.values, function(values) {
                            angular.forEach(values, function(value) {
                                promise = $http.delete(urls.values + value.id + '/');
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
                    promise = $http.put(urls.valuesets + valueset.id + '/', valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);
                    });
                } else {
                    // create a new valueset
                    promise = $http.post(urls.valuesets, valueset).success(function(response) {
                        // update the local valueset with the response from the server
                        angular.extend(valueset, response);
                    });
                }
            }

            promises.push(promise);
        });

        return $q.all(promises);
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
            fetchCatalog();
        });
    };

    service.prev = function() {
        if (service.entity.prev !== null) {
            back = true;
            fetchQuestionEntity(service.entity.prev);
        }
    };

    service.next = function() {
        if (service.entity.next !== null) {
            fetchQuestionEntity(service.entity.next);
        }
    };

    service.jump = function(item) {
        if (angular.isDefined(item.subsections)) {

            // this is a section
            fetchQuestionEntity(item.subsections[0].entities[0].id);

        } else if (angular.isDefined(item.entities)) {

            // this is a subsection
            fetchQuestionEntity(item.entities[0].id);

        }
    };

    service.save = function(proceed) {

        if (service.entity.is_set) {
            storeValueSets().then(function() {
                var promises = [];

                angular.forEach(service.valuesets, function(valueset, index) {
                    promises.push(storeValues(valueset));
                });

                if (angular.isDefined(proceed) && proceed) {
                    var i = getValueSetIndex();
                    if (angular.isDefined(service.valuesets[i + 1])) {
                        $q.all(promises).then(function() {
                            service.values = service.valuesets[i + 1].values;
                            $window.scrollTo(0, 0);
                        });
                    } else {
                        $q.all(promises).then(function() {
                            service.next();
                        });
                    }
                }
            });
        } else {
            storeValues().then(function() {
                if (angular.isDefined(proceed) && proceed) {
                    service.next();
                }
            });
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
