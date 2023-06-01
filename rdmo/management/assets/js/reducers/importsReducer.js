import isArray from 'lodash/isArray'
import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import { buildUri } from '../utils/elements'


const initialState = {
  elements: [],
  errors: [],
  success: false
}

export default function importsReducer(state = initialState, action) {
  let index, elements, elementsMap = {}

  switch(action.type) {
    // upload file
    case 'import/uploadFileInit':
    case 'elements/fetchElementsInit':
    case 'elements/fetchElementInit':
      return {...state, elements: [], errors: [], success: false}
    case 'import/uploadFileSuccess':
      return {...state, elements: action.elements.map(element => {
        if (['questions.catalogs', 'tasks.task', 'views.view'].includes(element.model)) {
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
      return {...state, elements: action.elements, success: true}
    case 'import/importElementsError':
      return {...state, errors: action.error.errors}

    // update element
    case 'import/updateElement':
      index = state.elements.findIndex(element => element == action.element)
      if (index > -1) {
        const elements = [...state.elements]
        elements[index] = {...elements[index], ...action.values}
        elements[index].uri = buildUri(elements[index])
        return {...state, elements}
      } else {
        return state
      }
    case 'import/selectElements':
      return {...state, elements: state.elements.map(element => {
        return {...element, import: action.value}
      })}
    case 'import/updateUriPrefix':
      elements = state.elements.map(element => {
        element.uri_prefix = action.uriPrefix

        // compute a new uri and store it in the elementMap
        element.uri = elementsMap[element.uri] = buildUri(element)

        return element
      })

      // loop over element fields and also update sub and sub-sub uris,
      // which are in the map, i.e. are imported as well
      elements.forEach(element => {
        Object.keys(element).forEach(key => {
          const subelement = element[key]
          if (!isNil(subelement)) {
            if (isArray(subelement)) {
              subelement.forEach(subsubelement => {
                if (!isUndefined(elementsMap[subsubelement.uri])) {
                  subsubelement.uri = elementsMap[subsubelement.uri]
                }
              })
            } else if (!isUndefined(elementsMap[subelement.uri])) {
              subelement.uri = elementsMap[subelement.uri]
            }
          }
        })
      })

      return {...state, elements}
    case 'import/resetElements':
      return {...state, elements: []}
    default:
      return state
  }
}
