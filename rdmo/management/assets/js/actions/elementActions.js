import isNil from 'lodash/isNil'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

import ConditionApi from '../api/ConditionApi'
import DomainApi from '../api/DomainApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'

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

export function fetchOptionsets() {
  return function(dispatch) {
    return OptionsApi.fetchOptionsets(true)
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
      dispatch(stopPending())
      dispatch(fetchElementsSuccess({
        element, groups, sites
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
    ]).then(([element]) => {
      dispatch(stopPending())
      dispatch(fetchElementsSuccess({
        element
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(fetchElementError(error))
    })
  }
}

export function fetchPage() {
  return function(dispatch) {
    return Promise.all([
      QuestionsApi.fetchPage(id),
      ConditionApi.fetchConditions(),
      DomainApi.fetchAttributes(),
    ]).then(([element, condtitions, attributes]) => {
      dispatch(stopPending())
      dispatch(fetchElementsSuccess({
        element, attributes, condtitions
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
      ConditionApi.fetchConditions(),
    ]).then(([element, condtitions]) => {
      dispatch(stopPending())
      dispatch(fetchElementsSuccess({
        element, condtitions
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
      QuestionsApi.fetchWidgetTypes(),
      QuestionsApi.fetchValueTypes(),
      DomainApi.fetchAttributes(),
      OptionsApi.fetchOptionsets(),
      OptionsApi.fetchOptions(),
    ]).then(([element, widgetTypes, valueTypes, attributes, optionsets, options]) => {
      dispatch(stopPending())
      dispatch(fetchElementsSuccess({
        element, widgetTypes, valueTypes, attributes, optionsets, options
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
      .then(catalog => {
        dispatch(stopPending())
        dispatch(storeElementSuccess({ catalog }))
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
      .then(section => {
        dispatch(stopPending())
        dispatch(storeElementSuccess({ section }))
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
      .then(page => {
        dispatch(stopPending())
        dispatch(storeElementSuccess({ page }))
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
      .then(questionset => {
        dispatch(stopPending())
        dispatch(storeElementSuccess({ questionset }))
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
      .then(question => {
        dispatch(stopPending())
        dispatch(storeElementSuccess({ question }))
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
