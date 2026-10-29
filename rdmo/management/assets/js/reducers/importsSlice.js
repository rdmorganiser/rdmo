import isArray from 'lodash/isArray'
import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import { processElementDiffs } from '../utils/diff'
import { buildPathForAttribute, buildUri } from '../utils/elements'

import { actions as elementActions } from './elementsSlice'
import { createSlice, original } from '@reduxjs/toolkit'

const initialState = {
  elements: [],
  errors: [],
  success: false,
  file: null
}

const resetImportState = (state) => {
  state.elements = []
  state.errors = []
  state.success = false
}

const setErrors = (state, action) => {
  state.errors = action.payload.errors
}

const keepState = state => state

const importsSlice = createSlice({
  name: 'imports',
  initialState,
  reducers: {
    uploadFileInit(state, action) {
      return { ...state, ...initialState, file: action.payload }
    },
    uploadFileSuccess(state, action) {
      state.elements = action.payload.map(element => {
        element = processElementDiffs(element)
        if (['questions.catalogs', 'tasks.task', 'views.view'].includes(element.model)) {
          element.available = true
        }
        element.show = false
        element.import = true
        return element
      })
    },
    uploadFileError: setErrors,
    importElementsInit: keepState,
    importElementsSuccess(state, action) {
      state.elements = action.payload.map(element => processElementDiffs(element))
      state.success = true
    },
    importElementsError: setErrors,
    updateElement(state, action) {
      const { element, values } = action.payload
      const index = original(state.elements).indexOf(element)
      if (index > -1) {
        const updatedElement = { ...state.elements[index], ...values }
        if (updatedElement.model === 'domain.attribute') {
          updatedElement.path = buildPathForAttribute(updatedElement.key,
            updatedElement.parent ? updatedElement.parent.uri : null)
        }
        const newUri = buildUri(updatedElement)
        if (!isNil(newUri)) {
          updatedElement.uri = newUri
        }
        state.elements[index] = updatedElement
      }
    },
    selectElements(state, action) {
      state.elements.forEach(element => {
        element.import = action.payload
      })
    },
    selectChangedElements(state, action) {
      state.elements.forEach(element => {
        if (element.changed || element.created) {
          element.import = action.payload
        } else if (action.payload) {
          element.import = !action.payload
        }
      })
    },
    showElements(state, action) {
      state.elements.forEach(element => {
        element.show = action.payload
      })
    },
    showChangedElements(state, action) {
      state.elements.forEach(element => {
        if (element.changed || element.created) {
          element.show = action.payload
        } else if (action.payload) {
          element.show = !action.payload
        }
      })
    },
    updateUriPrefix(state, action) {
      const elementsMap = {}
      state.elements.forEach(element => {
        element.uri_prefix = action.payload

        // compute a new uri and store it in the elementMap
        const newUri = buildUri(element)
        if (!isNil(newUri)) {
          element.uri = elementsMap[element.uri] = newUri
        }
      })

      // loop over element fields and also update sub and sub-sub uris,
      // which are in the map, i.e. are imported as well
      state.elements.forEach(element => {
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
    },
    resetElements(state) {
      state.elements = []
    }
  },
  extraReducers: builder => {
    builder.addCase(elementActions.fetchElementsInit, resetImportState)
    builder.addCase(elementActions.fetchElementInit, resetImportState)
  }
})

export const actions = importsSlice.actions

export default importsSlice.reducer
