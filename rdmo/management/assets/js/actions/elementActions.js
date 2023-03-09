import isNil from 'lodash/isNil'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

import ConditionsApi from '../api/ConditionsApi'
import DomainApi from '../api/DomainApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'
import TasksApi from '../api/TasksApi'
import ViewsApi from '../api/ViewsApi'

import { updateLocation } from '../utils/location'

import { startPending, stopPending } from '../actions/configActions'

export function fetchElements(elementType) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType)

    dispatch(fetchElementsInit(elementType))
    dispatch(startPending())

    switch (elementType) {
      case 'catalogs':
        dispatch(fetchCatalogs())
        break
      case 'sections':
        dispatch(fetchSections())
        break
      case 'pages':
        dispatch(fetchPages())
        break
      case 'questionsets':
        dispatch(fetchQuestionSets())
        break
      case 'questions':
        dispatch(fetchQuestions())
        break
      case 'attributes':
        dispatch(fetchAttributes())
        break
      case 'optionsets':
        dispatch(fetchOptionSets())
        break
      case 'options':
        dispatch(fetchOptions())
        break
      case 'conditions':
        dispatch(fetchConditions())
        break
      case 'tasks':
        dispatch(fetchTasks())
        break
      case 'views':
        dispatch(fetchViews())
        break
      default:
        dispatch(stopPending())
    }
  }
}

export function fetchElementsInit(elementType) {
  return {type: 'elements/fetchElementsInit', elementType}
}

export function fetchElementsSuccess(elements) {
  return {type: 'elements/fetchElementsSuccess', elements}
}

export function fetchElementsError(error) {
  return {type: 'elements/fetchElementsError', error}
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs(true)
      .then(catalogs => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ catalogs }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchSections() {
  return function(dispatch) {
    return QuestionsApi.fetchSections(true)
      .then(sections => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ sections }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchPages() {
  return function(dispatch) {
    return QuestionsApi.fetchPages(true)
      .then(pages => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ pages }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchQuestionSets() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestionSets(true)
      .then(questionsets => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ questionsets }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchQuestions() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestions(true)
      .then(questions => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ questions }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchAttributes() {
  return function(dispatch) {
    return DomainApi.fetchAttributes(true)
      .then(attributes => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ attributes }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchOptionSets() {
  return function(dispatch) {
    return OptionsApi.fetchOptionSets(true)
      .then(optionsets => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ optionsets }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchOptions() {
  return function(dispatch) {
    return OptionsApi.fetchOptions(true)
      .then(options => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ options }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchConditions() {
  return function(dispatch) {
    return ConditionsApi.fetchConditions(true)
      .then(conditions => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ conditions }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchTasks() {
  return function(dispatch) {
    return TasksApi.fetchTasks(true)
      .then(tasks => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ tasks }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

export function fetchViews() {
  return function(dispatch) {
    return ViewsApi.fetchViews(true)
      .then(views => {
        dispatch(stopPending())
        dispatch(fetchElementsSuccess({ views }))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(fetchElementsError(error))
      })
  }
}

// fetch element

export function fetchElement(elementType, elementId) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType, elementId)

    dispatch(fetchElementsInit(elementType, elementId))
    dispatch(startPending())

    switch (elementType) {
      case 'catalogs':
        dispatch(fetchCatalog(elementId))
        break
      case 'sections':
        dispatch(fetchSection(elementId))
        break
      case 'pages':
        dispatch(fetchPage(elementId))
        break
      case 'questionsets':
        dispatch(fetchQuestionSet(elementId))
        break
      case 'questions':
        dispatch(fetchQuestion(elementId))
        break
      case 'attributes':
        dispatch(fetchAttribute(elementId))
        break
      case 'optionsets':
        dispatch(fetchOptionSet(elementId))
        break
      case 'options':
        dispatch(fetchOption(elementId))
        break
      case 'conditions':
        dispatch(fetchCondition(elementId))
        break
      case 'tasks':
        dispatch(fetchTask(elementId))
        break
      case 'views':
        dispatch(fetchView(elementId))
        break
      default:
        dispatch(stopPending())
    }
  }
}

export function fetchElementInit(elementType, elementId) {
  return {type: 'elements/fetchElementInit', elementType, elementId}
}

export function fetchElementSuccess(elements) {
  return {type: 'elements/fetchElementSuccess', elements}
}

export function fetchElementError(error) {
  return {type: 'elements/fetchElementError', error}
}

export function fetchCatalog(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchCatalog(id),
      QuestionsApi.fetchSections('index'),
      CoreApi.fetchGroups(),
      CoreApi.fetchSites(),
    ]).then(([element, sections, groups, sites]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, sections, groups, sites
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchSection(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchSection(id),
      QuestionsApi.fetchPages('index'),
    ]).then(([element, pages]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, pages
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchPage(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchPage(id),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchQuestionSets('index'),
      QuestionsApi.fetchQuestions('index')
    ]).then(([element, attributes, conditions, questionsets, questions]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, attributes, conditions, questionsets, questions
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchQuestionSet(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchQuestionSet(id),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchQuestionSets('index'),
      QuestionsApi.fetchQuestions('index')
    ]).then(([element, attributes, conditions, questionsets, questions]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, attributes, conditions, questionsets, questions
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchQuestion(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchQuestion(id),
      DomainApi.fetchAttributes('index'),
      OptionsApi.fetchOptionSets('index'),
      OptionsApi.fetchOptions('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchWidgetTypes(),
      QuestionsApi.fetchValueTypes()
    ]).then(([element, attributes, optionsets, options, conditions, widgetTypes, valueTypes]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, attributes, optionsets, options, conditions, widgetTypes, valueTypes
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchAttribute(id) {
  return function(dispatch) {
    return Promise.all([
      DomainApi.fetchAttribute(id),
      DomainApi.fetchAttributes('index'),
    ]).then(([element, attributes]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, attributes
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchOptionSet(id) {
  return function(dispatch) {
    return Promise.all([
      OptionsApi.fetchOptionSet(id),
      OptionsApi.fetchOptions('index'),
      OptionsApi.fetchProviders(),
    ]).then(([element, options, providers]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, options, providers
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchOption(id) {
  return function(dispatch) {
    return Promise.all([
      OptionsApi.fetchOption(id),
      OptionsApi.fetchOptionSets('index'),
    ]).then(([element, optionsets]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, optionsets
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchCondition(id) {
  return function(dispatch) {
    return Promise.all([
      ConditionsApi.fetchCondition(id),
      ConditionsApi.fetchRelations(),
      DomainApi.fetchAttributes('index'),
      OptionsApi.fetchOptions('index'),
    ]).then(([element, relations, attributes, options]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, relations, attributes, options
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchTask(id) {
  return function(dispatch) {
    return Promise.all([
      TasksApi.fetchTask(id),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchCatalogs('index'),
      CoreApi.fetchSites(),
      CoreApi.fetchGroups()
    ]).then(([element, attributes, conditions, catalogs, sites, groups]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, attributes, conditions, catalogs, sites, groups
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchView(id) {
  return function(dispatch) {
    return Promise.all([
      ViewsApi.fetchView(id),
      QuestionsApi.fetchCatalogs('index'),
      CoreApi.fetchSites(),
      CoreApi.fetchGroups()
    ]).then(([element, catalogs, sites, groups]) => {
      dispatch(stopPending())
      dispatch(fetchElementSuccess({
        element, sites, groups, catalogs
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

// store element

export function storeElement(elementType, element) {
  return function(dispatch, getState) {
    dispatch(storeElementInit(element))
    dispatch(startPending())

    switch (elementType) {
      case 'catalogs':
        dispatch(storeCatalog(element))
        break
      case 'sections':
        dispatch(storeSection(element))
        break
      case 'pages':
        dispatch(storePage(element))
        break
      case 'questionsets':
        dispatch(storeQuestionSet(element))
        break
      case 'questions':
        dispatch(storeQuestion(element))
        break
      case 'attributes':
        dispatch(storeAttribute(element))
        break
      case 'optionsets':
        dispatch(storeOptionSet(element))
        break
      case 'options':
        dispatch(storeOption(element))
        break
      case 'conditions':
        dispatch(storeCondition(element))
        break
      case 'tasks':
        dispatch(storeTask(element))
        break
      case 'views':
        dispatch(storeView(element))
    }
  }
}

export function storeElementInit(element) {
  return {type: 'elements/storeElementInit', element}
}

export function storeElementSuccess(element) {
  return {type: 'elements/storeElementSuccess', element}
}

export function storeElementError(error) {
  return {type: 'elements/storeElementError', error}
}

export function storeCatalog(catalog) {
  return function(dispatch) {
    return QuestionsApi.storeCatalog(catalog)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeSection(section) {
  return function(dispatch) {
    return QuestionsApi.storeSection(section)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storePage(page) {
  return function(dispatch) {
    return QuestionsApi.storePage(page)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeQuestionSet(questionset) {
  return function(dispatch) {
    return QuestionsApi.storeQuestionSet(questionset)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeQuestion(question) {
  return function(dispatch) {
    return QuestionsApi.storeQuestion(question)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeAttribute(attribute) {
  return function(dispatch) {
    return DomainApi.storeAttribute(attribute)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeOptionSet(optionset) {
  return function(dispatch) {
    return OptionsApi.storeOptionSet(optionset)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeOption(option) {
  return function(dispatch) {
    return OptionsApi.storeOption(option)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeCondition(condition) {
  return function(dispatch) {
    return ConditionsApi.storeCondition(condition)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeTask(task) {
  return function(dispatch) {
    return TasksApi.storeTask(task)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

export function storeView(view) {
  return function(dispatch) {
    return ViewsApi.storeView(view)
      .then(element => {
        dispatch(stopPending())
        dispatch(storeElementSuccess(element))
      })
      .catch(error => {
        dispatch(stopPending())
        dispatch(storeElementError(error))
      })
  }
}

// update elements

export function updateElement(element, field, value) {
  return {type: 'elements/updateElement', element, field, value}
}
