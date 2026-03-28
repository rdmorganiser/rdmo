import isNil from 'lodash/isNil'

import * as actionTypes from '../actions/actionTypes'
import { resetElement, updateElement } from '../utils/elements'

const initialState = {
  elementType: null,
  elementId: null,
  element: null,
  errors: {},
  conditions: [],
  attributes: [],
  optionsets: [],
  options: [],
  catalogs: [],
  sections: [],
  pages: [],
  questionsets: [],
  questions: [],
  widgetTypes: [],
  valueTypes: [],
  tasks: [],
  views: []
}

export default function elementsReducer(state = initialState, action) {
  switch(action.type) {
    // fetch elements
    case actionTypes.FETCH_ELEMENTS_INIT:
      return {
        ...state,
        [action.elementType]: [],
        elementType: action.elementType,
        elementId: null,
        elementAction: null,
        element: null,
        parent: null,
        errors: {}
      }
    case actionTypes.FETCH_ELEMENTS_SUCCESS:
      return {...state, ...action.elements}
    case actionTypes.FETCH_ELEMENTS_ERROR:
      return {...state, errors: action.error.errors}

    // fetch element
    case actionTypes.FETCH_ELEMENT_INIT:
      return {
        ...state,
        elementType: action.elementType,
        elementId: action.elementId,
        elementAction: action.elementAction,
        element: null,
        parent: null,
        errors: {}
      }
    case actionTypes.FETCH_ELEMENT_SUCCESS:
      return {...state, ...action.elements}
    case actionTypes.FETCH_ELEMENT_ERROR:
      return {...state, errors: action.error.errors}

    // store element
    case actionTypes.STORE_ELEMENT_INIT:
      if (isNil(state.element)) {
        return state
      } else {
        // resetElements will apply the new order, when storing the element after drag and drop
        return {...state, element: resetElement(state.element)}
      }
    case actionTypes.STORE_ELEMENT_ERROR:
      if (isNil(state.element) || state.elementAction == 'nested') {
        // create a fake element with just the id and the model and the error for updateElement works,
        // but the element won't get updated in the view
        action.element = {id: action.element.id, model: action.element.model, errors: action.error.errors}
      } else {
        action.element.errors = action.error.errors
      }
      // there is not break here on purpose
    case actionTypes.STORE_ELEMENT_SUCCESS:  // eslint-disable-line no-fallthrough
      if (isNil(state.element)) {
        return {
          ...state,
          [state.elementType]: state[state.elementType].map(element => updateElement(element, action.element))
        }
      } else if (state.elementAction == 'nested') {
        return {...state, element: updateElement(state.element, action.element)}
      } else {
        return {...state, element: action.element}
      }

    // create element
    case actionTypes.CREATE_ELEMENT_INIT:
      return {
        ...state,
        elementType: action.elementType,
        elementId: null,
        elementAction: 'create',
        element: null,
        parent: null,
        errors: {}
      }
    case actionTypes.CREATE_ELEMENT_SUCCESS:
      return {...state, ...action.elements}
    case actionTypes.CREATE_ELEMENT_ERROR:
      return {...state, errors: action.error.errors}

    // delete element
    case actionTypes.DELETE_ELEMENT_INIT:
      return state

    case actionTypes.DELETE_ELEMENT_SUCCESS:
      return state

    case actionTypes.DELETE_ELEMENT_ERROR:
      return {...state, errors: action.error.errors}

    // update element
    case actionTypes.UPDATE_ELEMENT:
      return {...state, element: {...action.element, ...action.values}}

    default:
      return state
  }
}
