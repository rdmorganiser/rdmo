import isArray from 'lodash/isArray'
import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import * as actionTypes from '../actions/actionTypes'
import { processElementDiffs } from '../utils/diff'
import { buildPathForAttribute, buildUri } from '../utils/elements'


const initialState = {
  elements: [],
  errors: [],
  success: false,
  file: null
}

export default function importsReducer(state = initialState, action) {
  let index, elements, elementsMap = {}

  switch (action.type) {
    case actionTypes.FETCH_ELEMENTS_INIT:
    case actionTypes.FETCH_ELEMENT_INIT:
      return { ...state, elements: [], errors: [], success: false }

    // upload file
    case actionTypes.UPLOAD_IMPORT_FILE_INIT:
      return { ...state, ...initialState, file: action.file }
    case actionTypes.UPLOAD_IMPORT_FILE_SUCCESS:
      return {
        ...state, elements: action.elements.map(element => {
          element = processElementDiffs(element)
          if (['questions.catalogs', 'tasks.task', 'views.view'].includes(element.model)) {
            element.available = true
          }
          element.show = false
          element.import = true
          return element
        })
      }
    case actionTypes.UPLOAD_IMPORT_FILE_ERROR:
      return { ...state, errors: action.error.errors }

    // import elements
    case actionTypes.IMPORT_ELEMENTS_SUCCESS:
      return { ...state, elements: action.elements.map(element => processElementDiffs(element)), success: true }
    case actionTypes.IMPORT_ELEMENTS_ERROR:
      return { ...state, errors: action.error.errors }

    // update element
    case actionTypes.UPDATE_IMPORT_ELEMENT:
      index = state.elements.findIndex(element => element === action.element)
      if (index > -1) {
        const elements = [...state.elements]
        elements[index] = { ...elements[index], ...action.values }
        if (elements[index].model === 'domain.attribute') {
          elements[index].path =
            buildPathForAttribute(elements[index].key, elements[index].parent ? elements[index].parent.uri : null)
        }
        const newUri = buildUri(elements[index])
        if (!isNil(newUri)) {
          elements[index].uri = newUri
        }
        return { ...state, elements }
      } else {
        return state
      }
    case actionTypes.SELECT_IMPORT_ELEMENTS:
      return {
        ...state, elements: state.elements.map(element => {
          return { ...element, import: action.value }
        })
      }
    case actionTypes.SELECT_CHANGED_IMPORT_ELEMENTS:
      return {
        ...state, elements: state.elements.map(element => {
          if (element.changed || element.created) {
            return { ...element, import: action.value }
          }
          else if (action.value) { return { ...element, import: !action.value } }
          else { return element }
        }
        )
      }
    case actionTypes.SHOW_IMPORT_ELEMENTS:
      return {
        ...state, elements: state.elements.map(element => {
          return { ...element, show: action.value }
        })
      }
    case actionTypes.SHOW_CHANGED_IMPORT_ELEMENTS:
      return {
        ...state, elements: state.elements.map(element => {
          if (element.changed || element.created) {
            return { ...element, show: action.value }
          }
          else if (action.value) { return { ...element, show: !action.value } }
          else { return element }
        }
        )
      }
    case actionTypes.UPDATE_IMPORT_URI_PREFIX:
      elements = state.elements.map(element => {
        element.uri_prefix = action.uriPrefix

        // compute a new uri and store it in the elementMap
        const newUri = buildUri(element)
        if (!isNil(newUri)) {
          element.uri = elementsMap[element.uri] = newUri
        }

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

      return { ...state, elements }
    case actionTypes.RESET_IMPORT_ELEMENTS:
      return { ...state, elements: [] }
    default:
      return state
  }
}
