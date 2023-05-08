import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'

import { updateElement, resetElement } from '../utils/elements'

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

      // remove the id when copying
      if (state.elementAction == 'copy') {
        action.elements.element.id = null
      }

      return {...state, ...action.elements}
    case 'elements/fetchElementError':
      return {...state, errors: action.error.errors}

    // store element
    case 'elements/storeElementInit':
      if (isNil(state.element)) {
        return state
      } else {
        return {...state, element: resetElement(state.element)}
      }
    case 'elements/storeElementError':
      if (isNil(state.element) || state.elementAction == 'nested') {
        // create a fake element with just the uri and the error for updateElement works,
        // but the element won't get updated in the view
        action.element = {uri: action.element.uri, errors: action.error.errors}
      } else {
        action.element.errors = action.error.errors
      }
    case 'elements/storeElementSuccess':
      if (isNil(state.element)) {
        return {...state,
          [state.elementType]: state[state.elementType].map(element => updateElement(element, action.element))
        }
      } else if (state.elementAction == 'nested') {
        return {...state, element: updateElement(state.element, action.element)}
      } else {
        // let the element know what type it is
        action.element.type = state.elementType

        return {...state, element: action.element}
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
      return {...state, element: {...action.element, ...action.values}}

    default:
      return state
  }
}
