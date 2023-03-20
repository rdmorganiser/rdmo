import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'

import { replaceElement } from '../utils/elements'

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
    case 'elements/fetchElementsInit':
      return {...state,
        [action.elementType]: [],
        elementType: action.elementType,
        elementId: null,
        elementAction: null,
        element: null,
        errors: {}
      }
    case 'elements/fetchElementsSuccess':
      return {...state, ...action.elements}
    case 'elements/fetchElementsError':
      return {...state, errors: action.error.errors}

    // fetch element
    case 'elements/fetchElementInit':
      return {...state,
        elementType: action.elementType,
        elementId: action.elementId,
        elementAction: action.elementAction,
        element: null,
        errors: {}
      }
    case 'elements/fetchElementSuccess':
      // let the element know what type it is
      action.elements.element.type = state.elementType

      return {...state, ...action.elements}
    case 'elements/fetchElementError':
      return {...state, errors: action.error.errors}

    // store element
    case 'elements/storeElementInit':
      if (isNil(state.element)) {
        return state
      } else if (state.elementAction == 'nested') {
        return state
      } else {
        return {...state, element: {...action.element, errors: {}}}
      }
    case 'elements/storeElementSuccess':

      if (isNil(state.element)) {
        const elements = state[state.elementType]
        return {...state,
          [state.elementType]: replaceElement(elements, action.element)
        }
      } else if (state.elementAction == 'nested') {
        if (state.element.uri == action.element.uri) {
          return {...state, element: {...state.element, ...action.element}}
        } else {
          const elements = state.element.elements
          return {...state, element: {...state.element, elements: replaceElement(elements, action.element)}}
        }
      } else {
        // let the element know what type it is
        action.element.type = state.elementType

        return {...state, element: action.element}
      }
    case 'elements/storeElementError':
      if (isNil(state.element)) {
        return state
      } else {
        return {...state, ...{
          element: {...action.element, errors: action.error.errors}
        }}
      }

    // create element
    case 'elements/createElementInit':
      return {
        ...state,
        elementType: action.elementType,
        elementId: null,
        elementAction: 'create',
        element: null,
        errors: {}
      }
    case 'elements/createElementSuccess':
      // let the element know what type it is
      action.elements.element.type = state.elementType

      return {...state, ...action.elements}
    case 'elements/createElementError':
      return {...state, errors: action.error.errors}


    // delete element
    case 'elements/deleteElementInit':
      return state

    case 'elements/deleteElementSuccess':
      return state

    case 'elements/deleteElementError':
      return {...state, errors: action.error.errors}

    // update element
    case 'elements/updateElement':
      return {...state, element: {...action.element, [action.field]: action.value }}

    default:
      return state
  }
}
