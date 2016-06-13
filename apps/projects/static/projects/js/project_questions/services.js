angular.module('project_questions')

.factory('QuestionsService', ['$http', '$timeout', '$location', '$filter', '$q', '$window', function($http, $timeout, $location, $filter, $q, $window) {

    service = {};

    /* private varilables */

    var baseurl = angular.element('meta[name="baseurl"]').attr('content');

    var urls = {
        'projects': baseurl + 'api/projects/projects/',
        'values': baseurl + 'api/projects/values/',
        'catalog': baseurl + 'api/questions/catalogs/',
        'question_entities': baseurl + 'api/questions/entities/'
    };

    var back = false;

    /* private methods */

    function factory(ressource, parent) {
        if (ressource === 'values') {
            var value = {
                'text': '',
                'option': null,
                'snapshot': service.project.current_snapshot
            };

            if (angular.isDefined(parent) && parent) {
                value.attribute = parent.attribute.id;
            } else {
                value.attribute = service.entity.attribute.id;
            }

            return value;

        } else if (ressource === 'valuesets') {
            return {
                'values': {},
            };
        }
    }

    function initCheckbox(values, options, parent) {
        var checkbox_values = [];

        angular.forEach(options, function(option) {
            var filter = $filter('filter')(values, function(value, index, array) {
                return value.option === option.id;
            });

            var value;
            if (filter.length === 1) {
                value = filter[0];
                value.removed = false;
            } else {
                value = factory('values', parent);
                value.removed = true;
                value.option = option.id;
            }

            checkbox_values.push(value);
        });

        return checkbox_values;
    }

    function initWidget(question, value) {

        if (question.widget_type === 'radio') {
            value.input = {};

            angular.forEach(question.attribute.options, function(option) {
                if (option.additional_input) {
                    if (value.option === option.id) {
                        value.input[option.id] = value.text;
                    } else {
                        value.input[option.id] = '';
                    }
                }
            });
        }

        if (question.widget_type === 'range') {
            if (!value.text) {
                value.text = '0';
            }
        }

        if (question.widget_type === 'date') {
            $timeout(function() {
                $('.datepicker').datetimepicker({
                    format: 'YYYY-MM-DD'
                }).on('dp.change', function () {
                    $('.datepicker input').trigger('input');
                });
            });
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

                    fetchValues();
                }
            });
        });
    }

    function fetchValues() {

        service.values = {};

        if (service.entity.is_set) {

            var promises = [];

            service.valuesets = [factory('valuesets')];

            angular.forEach(service.questions, function(question, index) {

                var promise = $http.get(urls.values, {
                    params: {
                        snapshot: service.project.current_snapshot,
                        attribute: question.attribute.id
                    }
                }).success(function(response) {

                    angular.forEach(response, function(value) {
                        if (angular.isUndefined(service.valuesets[value.set_index])) {
                            while (service.valuesets.length < value.set_index + 1) {
                                service.valuesets.push(factory('valuesets'));
                            }
                        }

                        if (angular.isDefined(service.valuesets[value.set_index].values[question.attribute.id])) {
                            service.valuesets[value.set_index].values[question.attribute.id].push(value);
                        } else {
                            service.valuesets[value.set_index].values[question.attribute.id] = [value];
                        }
                    });

                });

                promises.push(promise);
            });

            return $q.all(promises).then(function() {
                angular.forEach(service.valuesets, function(valueset, index) {

                    angular.forEach(service.questions, function(question, index) {

                        if (question.widget_type === 'checkbox') {
                            if (angular.isUndefined(valueset.values[question.attribute.id])) {
                                valueset.values[question.attribute.id] = [];
                            }
                            valueset.values[question.attribute.id] = initCheckbox(
                                valueset.values[question.attribute.id],
                                question.attribute.options,
                                question
                            );
                        } else {
                            if (angular.isUndefined(valueset.values[question.attribute.id])) {
                                valueset.values[question.attribute.id] = [factory('values', question)];
                            }
                        }

                        angular.forEach(valueset.values[question.attribute.id], function(value) {
                            initWidget(question, value);
                        });
                    });

                });

                service.values = service.valuesets[0].values;
            });

        } else {
            return $http.get(urls.values, {
                params: {
                    snapshot: service.project.current_snapshot,
                    attribute: service.entity.attribute.id
                }
            }).success(function(response) {
                service.values[service.entity.attribute.id] = response;

                if (service.entity.widget_type === 'checkbox') {
                    service.values[service.entity.attribute.id] = initCheckbox(
                        service.values[service.entity.attribute.id],
                        service.entity.attribute.options
                    );
                } else {
                    if (service.values[service.entity.attribute.id].length < 1) {
                        service.values[service.entity.attribute.id].push(factory('values'));
                    }
                }

                angular.forEach(service.values[service.entity.attribute.id], function(value) {
                    initWidget(service.entity, value);
                });
            });
        }
    }

    function storeValues() {
        var promises = [];

        if (service.entity.is_set) {

            var set_index = 0;
            angular.forEach(service.valuesets, function(valueset) {
                angular.forEach(service.questions, function(question) {

                    var collection_index = 0;
                    angular.forEach(valueset.values[question.attribute.id], function(value, collection_index) {
                        var promise;

                        if (value.removed) {
                            // delete the value if it alredy exists on the server
                            if (angular.isDefined(value.id)) {
                                promise = $http.delete(urls.values + value.id + '/');
                            }
                        } else {
                            // store the current index in the list
                            value.set_index = set_index;
                            value.collection_index = collection_index;

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

                            collection_index++;
                        }

                        promises.push(promise);
                    });
                });

                if (!valueset.removed) {
                    set_index++;
                }
            });
        } else {
            angular.forEach(service.questions, function(question) {
                angular.forEach(service.values[question.attribute.id], function(value, index) {
                    var promise;

                    if (value.removed) {
                        // delete the value if it alredy exists on the server
                        if (angular.isDefined(value.id)) {
                            promise = $http.delete(urls.values + value.id + '/');
                        }
                    } else {
                        // store the current index in the list
                        value.collection_index = index;

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
        }

        return $q.all(promises);
    }

    function getValueSetIndex() {
        return $filter('filter')(service.valuesets, function(valueset, index, array) {
            return valueset.values == service.values;
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
        storeValues().then(function() {
            if (angular.isDefined(proceed) && proceed) {
                if (service.entity.is_set && service.entity.attribute_entity.is_collection) {
                    // var i = getValueSetIndex();
                    // if (angular.isDefined(service.valuesets[i + 1])) {
                    //     service.values = service.valuesets[i + 1].values;
                    //     $window.scrollTo(0, 0);
                    // } else {
                    //     service.next();
                    // }
                } else {
                    service.next();
                }
            }
        });
    };

    service.addValue = function(question) {
        var value = factory('values', question);

        //  add new value to service.values
        if (angular.isUndefined(service.values[question.attribute.id])) {
            service.values[question.attribute.id] = [value];
        } else {
            service.values[question.attribute.id].push(value);
        }

        initWidget(question, value);
    };

    service.removeValue = function(attribute_id, index) {
        service.values[attribute_id][index].removed = true;
    };

    service.addValueSet = function() {
        // create a new valueset
        var valueset = factory('valuesets');

        // add values for the new valueset
        angular.forEach(service.questions, function(question, index) {
            valueset.values[question.attribute.id] = [factory('values', question)];
        });

        // append the new valueset to the array of valuesets
        service.valuesets.push(valueset);

        // 'activate' the new valueset
        service.values = valueset.values;
    };


    service.removeValueSet = function() {
        // find current valueset
        var i = $filter('filter')(service.valuesets, function(valueset, index, array) {
            valueset.index = index;
            return valueset.values == service.values;
        })[0].index;

        // flag it for removal
        service.valuesets[i].removed = true;

        // flag all values as removed
        angular.forEach(service.questions, function(question) {
            angular.forEach(service.valuesets[i].values[question.attribute.id], function(value, collection_index) {
                value.removed = true;
            });
        });

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
