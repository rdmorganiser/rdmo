import isNil from 'lodash/isNil'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

import ConditionApi from '../api/ConditionApi'
import DomainApi from '../api/DomainApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'

import { updateLocation } from '../utils/location'

export function fetchElements(elementType) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType)

    dispatch(fetchElementsInit(elementType))

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

export function fetchAttributes() {
  return function(dispatch) {
    return DomainApi.fetchAttributes(true)
      .then(attributes => dispatch(fetchElementsSuccess({ attributes })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchOptionsets() {
  return function(dispatch) {
    return OptionsApi.fetchOptionsets(true)
      .then(optionsets => dispatch(fetchElementsSuccess({ optionsets })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchOptions() {
  return function(dispatch) {
    return OptionsApi.fetchOptions(true)
      .then(options => dispatch(fetchElementsSuccess({ options })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs(true)
      .then(catalogs => dispatch(fetchElementsSuccess({ catalogs })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchSections() {
  return function(dispatch) {
    return QuestionsApi.fetchSections(true)
      .then(sections => dispatch(fetchElementsSuccess({ sections })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchPages() {
  return function(dispatch) {
    return QuestionsApi.fetchPages(true)
      .then(pages => dispatch(fetchElementsSuccess({ pages })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchQuestionSets() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestionSets(true)
      .then(questionsets => dispatch(fetchElementsSuccess({ questionsets })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

export function fetchQuestions() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestions(true)
      .then(questions => dispatch(fetchElementsSuccess({ questions })))
      .catch(error => dispatch(fetchElementsError(error)))
  }
}

// fetch element

export function fetchElement(elementType, elementId) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType, elementId)

    dispatch(fetchElementsInit(elementType, elementId))

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
      CoreApi.fetchGroups(),
      CoreApi.fetchSites(),
    ]).then(([element, groups, sites]) => {
      dispatch(fetchElementsSuccess({
        element, groups, sites
      }))
    }).catch(error => dispatch(fetchElementError(error)))
  }
}

export function fetchSection(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchSection(id),
    ]).then(([element]) => {
      dispatch(fetchElementsSuccess({
        element
      }))
    }).catch(error => dispatch(fetchElementError(error)))
  }
}

export function fetchPage() {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchPage(id),
      ConditionApi.fetchConditions(),
      DomainApi.fetchAttributes(),
    ]).then(([element, condtitions, attributes]) => {
      dispatch(fetchElementsSuccess({
        element, attributes, condtitions
      }))
    }).catch(error => dispatch(fetchElementError(error)))
  }
}

export function fetchQuestionSet(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchQuestionSet(id),
      ConditionApi.fetchConditions(),
    ]).then(([element, condtitions]) => {
      dispatch(fetchElementsSuccess({
        element, condtitions
      }))
    }).catch(error => dispatch(fetchElementError(error)))
  }
}

export function fetchQuestion(id) {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchQuestion(id),
      QuestionsApi.fetchWidgetTypes(),
      QuestionsApi.fetchValueTypes(),
      DomainApi.fetchAttributes(),
      OptionsApi.fetchOptionsets(),
      OptionsApi.fetchOptions(),
    ]).then(([element, widgetTypes, valueTypes, attributes, optionsets, options]) => {
      dispatch(fetchElementsSuccess({
        element, widgetTypes, valueTypes, attributes, optionsets, options
      }))
    }).catch(error => dispatch(fetchElementError(error)))
  }
}

// store element

export function storeElement(elementType, element) {
  return function(dispatch, getState) {
    dispatch(storeElementInit(element))

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
      .then(catalogs => dispatch(storeElementSuccess({ catalog })))
      .catch(error => dispatch(storeElementError(error)))
  }
}

export function storeSection(section) {
  return function(dispatch) {
    return QuestionsApi.storeSection(section)
      .then(catalogs => dispatch(storeElementSuccess({ section })))
      .catch(error => dispatch(storeElementError(error)))
  }
}

export function storePage(page) {
  return function(dispatch) {
    return QuestionsApi.storePage(page)
      .then(catalogs => dispatch(storeElementSuccess({ page })))
      .catch(error => dispatch(storeElementError(error)))
  }
}

export function storeQuestionSet(questionset) {
  return function(dispatch) {
    return QuestionsApi.storeQuestionSet(questionset)
      .then(catalogs => dispatch(storeElementSuccess({ questionset })))
      .catch(error => dispatch(storeElementError(error)))
  }
}

export function storeQuestion(question) {
  return function(dispatch) {
    return QuestionsApi.storeQuestion(question)
      .then(catalogs => dispatch(storeElementSuccess({ question })))
      .catch(error => dispatch(storeElementError(error)))
  }
}

// update elements

export function updateElement(element, field, value) {
  return {type: 'elements/updateElement', element, field, value}
}
