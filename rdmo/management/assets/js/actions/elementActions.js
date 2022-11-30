import QuestionsApi from '../api/QuestionsApi'

import { updateLocation } from '../utils/location'
import { elementTypes } from '../constants/elements'

export function fetchElements(elementType) {
  return function(dispatch, getState) {
    if (elementType === '') {
      elementType = 'catalogs'
    }

    if (elementTypes.includes(elementType)) {
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
    } else {
      const error = interpolate(gettext('Invalid element type given ("%s").'), [elementType])
      dispatch(fetchElementsError([error]))
    }
  }
}

export function fetchElementsInit(elementType) {
  return {type: 'elements/fetchElementsInit', elementType }
}

export function fetchElementsSuccess(elements) {
  return {type: 'elements/fetchElementsSuccess', elements }
}

export function fetchElementsError(errors) {
  return {type: 'elements/fetchElementsError', errors}
}

export function fetchElement(elementType, elementId) {
  return {type: 'elements/fetchElement', elementType, elementId }
}

export function fetchElementSuccess(element) {
  return {type: 'elements/fetchElementSuccess', element}
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs(true)
      .then(elements => dispatch(fetchElementsSuccess(elements)))
      .catch(error => dispatch(fetchElementsError([error.message])))
  }
}

export function fetchSections() {
  return function(dispatch) {
    return QuestionsApi.fetchSections(true)
      .then(elements => dispatch(fetchElementsSuccess(elements)))
      .catch(error => dispatch(fetchElementsError([error.message])))
  }
}

export function fetchPages() {
  return function(dispatch) {
    return QuestionsApi.fetchPages(true)
      .then(elements => dispatch(fetchElementsSuccess(elements)))
      .catch(error => dispatch(fetchElementsError([error.message])))
  }
}

export function fetchQuestionSets() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestionSets(true)
      .then(elements => dispatch(fetchElementsSuccess(elements)))
      .catch(error => dispatch(fetchElementsError([error.message])))
  }
}

export function fetchQuestions() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestions(true)
      .then(elements => dispatch(fetchElementsSuccess(elements)))
      .catch(error => dispatch(fetchElementsError([error.message])))
  }
}
