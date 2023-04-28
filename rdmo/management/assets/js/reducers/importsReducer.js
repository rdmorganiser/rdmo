import uniqueId from 'lodash/uniqueId'

import { buildUri } from '../utils/elements'


const initialState = {
  elements: [],
  errors: []
}

export default function importsReducer(state = initialState, action) {
  switch(action.type) {
    // upload file
    case 'import/uploadFileInit':
      return {...state, elements: [], errors: []}
    case 'import/uploadFileSuccess':
      return {...state, elements: action.elements.map(element => {
        if (['catalogs', 'tasks', 'views'].includes(element.type)) {
          element.available = true
        }
        element.show = false
        element.import = true
        return element
      })}
    case 'import/uploadFileError':
      return {...state, errors: action.error.errors}

    // import elements
    case 'import/importElementsSuccess':
      return {...state, elements: []}
    case 'import/importElementsError':
      return {...state, errors: action.error.errors}

    // update element
    case 'import/updateElement':
      const index = state.elements.findIndex(element => element == action.element)
      if (index > -1) {
        const elements = [...state.elements]
        elements[index] = {...elements[index], ...action.values}
        elements[index].uri = buildUri(elements[index])
        return {...state, elements}
      }
    case 'import/updateElements':
      return {...state, elements: state.elements.map(element => {
        Object.assign(element, action.values)
        element.uri = buildUri(element)
        return element
      })}
    case 'import/resetElements':
      return {...state, elements: []}
    default:
      return state
  }
}
