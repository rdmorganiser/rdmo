import isUndefined from 'lodash/isUndefined'

const initialState = {
  elementType: null,
  elementId: null,
  element: null,
  warnings: {},
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
      return Object.assign({}, state, {
        [action.elementType]: [],
        elementType: action.elementType,
        elementId: null,
        element: null,
        warnings: {},
        errors: {}
      })
    case 'elements/fetchElementsSuccess':
      return Object.assign({}, state, action.elements)
    case 'elements/fetchElementsError':
      return Object.assign({}, state, {
        errors: action.error.errors
      })

    // fetch element
    case 'elements/fetchElementInit':
      return Object.assign({}, state, {
        elementType: action.elementType,
        elementId: action.elementId,
        element: null,
        warnings: {},
        errors: {}
      })
    case 'elements/fetchElementSuccess':
      // let the element know what type it is
      action.elements.element.type = state.elementType

      return Object.assign({}, state, action.elements)
    case 'elements/fetchElementError':
      return Object.assign({}, state, {
        errors: action.error.errors
      })

    // store element
    case 'elements/storeElementInit':
      return Object.assign({}, state, {
        errors: {}
      })
    case 'elements/storeElementSuccess':
      // let the element know what type it is
      action.element.type = state.elementType

      return Object.assign({}, state, {
        element: action.element
      })
    case 'elements/storeElementError':
      return Object.assign({}, state, {
        errors: action.error.errors
      })

    // update element
    case 'elements/updateElement':
      const element = Object.assign({}, action.element, {
        [action.field]: action.value
      })
      return Object.assign({}, state, {
        element: element
      })

    default:
      return state
  }
}
