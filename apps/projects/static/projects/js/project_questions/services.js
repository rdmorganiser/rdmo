angular.module('project_questions')

.factory('QuestionsService', ['$http', '$timeout', '$location', '$filter', '$q', '$window', function($http, $timeout, $location, $filter, $q, $window) {

    service = {
        values: null
    };

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

    function checkCondition(condition, value) {
        if (condition.relation === 'eq') {
            if (angular.isDefined(condition.target_option) && condition.target_option !== null) {
                return (condition.target_option == value.option);
            } else if (angular.isDefined(condition.target_text) && condition.target_text !== null) {
                return (condition.target_text == value.text);
            } else {
                return true;
            }
        } else if (condition.relation === 'neq') {
            if (angular.isDefined(condition.target_option) && condition.target_option !== null) {
                return (condition.target_option != value.option);
            } else if (angular.isDefined(condition.target_text) && condition.target_text !== null) {
                return (condition.target_text != value.text);
            } else {
                return true;
            }
        }
    }

    function fetchCatalog() {
        return $http.get(urls.catalog + service.project.catalog + '/', {
            params: {
                nested: true
            }
        }).success(function(response) {
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
                    attribute: condition.source_attribute
                };

                promises.push($http.get(urls.values, {'params': params}));
            });

            $q.all(promises).then(function(results) {
                var checks = [];
                var values = {};

                angular.forEach(results, function (result) {
                    values[result.config.params.attribute] = result.data;
                });

                angular.forEach(response.conditions, function (condition) {
                    angular.forEach(values[condition.source_attribute], function (value) {
                        checks.push(checkCondition(condition, value));
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

                    // gather attributes for this questionset
                    service.attributes = service.questions.map(function(question) {
                        return question.attribute;
                    });
                    if (service.entity.title_attribute) {
                        service.attributes.push(service.entity.title_attribute);
                    }

                    // store verbose set name
                    service.name = service.entity.attribute_entity.verbosename.name;
                    service.name_plural = service.entity.attribute_entity.verbosename.name_plural;

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

            // init valuesets array
            service.valuesets = [];

            // loop over attributes and fetch values from the server
            angular.forEach(service.attributes, function(attribute) {

                var promise = $http.get(urls.values, {
                    params: {
                        snapshot: service.project.current_snapshot,
                        attribute: attribute.id
                    }
                }).success(function(response) {

                    // loop over fetched values and sort them into valuesets
                    angular.forEach(response, function(value) {
                        // create a number of valuesets up to the one needed for this value
                        if (angular.isUndefined(service.valuesets[value.set_index])) {
                            while (service.valuesets.length < value.set_index + 1) {
                                service.valuesets.push(factory('valuesets'));
                            }
                        }

                        // add this value to the valueset
                        if (angular.isDefined(service.valuesets[value.set_index].values[attribute.id])) {
                            service.valuesets[value.set_index].values[attribute.id].push(value);
                        } else {
                            service.valuesets[value.set_index].values[attribute.id] = [value];
                        }
                    });

                });

                promises.push(promise);
            });

            return $q.all(promises).then(function() {

                // ensure at least one valueset for a non-collection questionset
                if (service.valuesets.length === 0 && !service.entity.attribute_entity.is_collection) {
                    service.valuesets.push(factory('valuesets'));
                }

                // loop over valuesets and questions to init values and widgets
                angular.forEach(service.valuesets, function(valueset) {
                    angular.forEach(service.questions, function(question) {

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

                // activate first valueset if there are any
                if (service.valuesets.length > 0) {
                    service.values = service.valuesets[0].values;
                } else {
                    service.values = null;
                }
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

    function storeValue(value, collection_index, set_index) {
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
        }

        return promise;
    }

    function storeValues() {
        var promises = [];

        if (service.entity.is_set) {

            var set_index = 0;
            angular.forEach(service.valuesets, function(valueset) {
                angular.forEach(service.attributes, function(attribute) {
                    angular.forEach(valueset.values[attribute.id], function(value, collection_index) {
                        promises.push(storeValue(value, collection_index, set_index));
                    });
                });

                if (!valueset.removed) {
                    set_index++;
                }
            });
        } else {
            angular.forEach(service.attributes, function(attribute) {
                angular.forEach(service.values[attribute.id], function(value, collection_index) {
                    promises.push(storeValue(value, collection_index, 0));
                });
            });
        }

        return $q.all(promises);
    }

    function getValueSetIndex() {
        return $filter('filter')(service.valuesets, function(valueset, index, array) {
            valueset.index = index;
            return valueset.values == service.values;
        })[0].index;
    }

    function getPrevActiveValueSetIndex(index) {
        var prev_active_index = null;
        for (var i = index - 1; i >= 0; i--) {
            if (angular.isUndefined(service.valuesets[i].removed) || !service.valuesets[i].removed) {
                prev_active_index = i;
                break;
            }
        }
        return prev_active_index;
    }

    function getNextActiveValueSetIndex(index) {
        var next_active_index = null;
        for (i = index + 1; i < service.valuesets.length; i++) {
            if (angular.isUndefined(service.valuesets[i].removed) || !service.valuesets[i].removed) {
                next_active_index = i;
                break;
            }
        }
        return next_active_index;
    }

    /* public methods */

    service.init = function(project_id, summary_url) {
        service.summary_url = summary_url;

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
                    var index = getValueSetIndex();

                    var new_index = getNextActiveValueSetIndex(index);
                    if (new_index === null) {
                        if (service.entity.next === null) {
                            $window.location = service.summary_url;
                        } else {
                            service.next();
                        }
                    } else {
                        service.values = service.valuesets[new_index].values;
                        $window.scrollTo(0, 0);
                    }
                } else {
                    if (service.entity.next === null) {
                        $window.location = service.summary_url;
                    } else {
                        service.next();
                    }
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

    service.openValueSetModal = function(create) {

        service.modal_values = {};
        service.modal_errors = {};

        if (angular.isDefined(create) && create) {
            // set the create flag on the modal_values
            service.modal_values.create = true;
        } else {
            // get the existing title if there is a value for that
            if (service.entity.title_attribute) {
                if (angular.isDefined(service.values[service.entity.title_attribute.id])) {
                    service.modal_values = angular.copy(service.values[service.entity.title_attribute.id][0]);
                }
            }
        }

        $timeout(function() {
            $('#valuesets-form-modal').modal('show');
        });
    };

    service.submitValueSetModal = function() {

        service.modal_errors = {};

        if (angular.isUndefined(service.modal_values.text) || !service.modal_values.text) {
            service.modal_errors.text = [];
            return;
        }

        // create a new valueset if the create flag was set
        if (angular.isDefined(service.modal_values.create) && service.modal_values.create) {
            service.addValueSet();
        }

        // create or update the value holding the id of the valuset
        if (service.entity.title_attribute) {
            if (angular.isUndefined(service.values[service.entity.title_attribute.id])) {
                service.values[service.entity.title_attribute.id] = [{
                    'snapshot': service.project.current_snapshot,
                    'attribute': service.entity.title_attribute.id,
                    'text': service.modal_values.text
                }];
            } else {
                service.values[service.entity.title_attribute.id][0] = angular.copy(service.modal_values);
            }
        }

        $timeout(function() {
            $('#valuesets-form-modal').modal('hide');
        });
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
        var index = getValueSetIndex();

        // flag it for removal
        service.valuesets[index].removed = true;

        // flag all values as removed
        angular.forEach(service.attributes, function(attribute) {
            angular.forEach(service.valuesets[index].values[attribute.id], function(value) {
                value.removed = true;
            });
        });

        // look for an non-removed valueset before the current one
        var new_index = getPrevActiveValueSetIndex(index);

        // if no was found, look  for an non-removed valueset after the current one
        if (new_index === null) {
            new_index = getNextActiveValueSetIndex(index);
        }

        // if there is still now new_index, set service.values to null, otherwise activate the valueset
        if (new_index === null) {
            service.values = null;
        } else {
            service.values = service.valuesets[new_index].values;
        }
    };

    return service;

}]);
