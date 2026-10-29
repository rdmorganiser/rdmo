import isNil from 'lodash/isNil'

import { resetElement, updateElement } from '../utils/elements'

import { createSlice } from '@reduxjs/toolkit'

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

const setElements = (state, action) => ({ ...state, ...action.payload })

const setErrors = (state, action) => {
  state.errors = action.payload.errors
}

const resetElementErrors = (state) => {
  if (!isNil(state.element)) {
    // resetElements will apply the new order, when storing the element after drag and drop
    state.element = resetElement(state.element)
  }
}

const setElement = (state, action) => {
  if (isNil(state.element)) {
    state[state.elementType] = state[state.elementType].map(element => updateElement(element, action.payload))
  } else if (state.elementAction == 'nested') {
    state.element = updateElement(state.element, action.payload)
  } else {
    state.element = action.payload
  }
}

const setElementErrors = (state, action) => {
  const { element, error } = action.payload
  let elementWithErrors

  if (isNil(state.element) || state.elementAction == 'nested') {
    // create a fake element with just the id and the model and the error for updateElement works,
    // but the element won't get updated in the view
    elementWithErrors = { id: element.id, model: element.model, errors: error.errors }
  } else {
    elementWithErrors = { ...element, errors: error.errors }
  }

  setElement(state, { payload: elementWithErrors })
}

const keepState = state => state

const elementsSlice = createSlice({
  name: 'elements',
  initialState,
  reducers: {
    fetchElementsInit(state, action) {
      state[action.payload] = []
      state.elementType = action.payload
      state.elementId = null
      state.elementAction = null
      state.element = null
      state.parent = null
      state.errors = {}
    },
    fetchElementsSuccess: setElements,
    fetchElementsError: setErrors,
    fetchElementInit(state, action) {
      const { elementType, elementId, elementAction } = action.payload
      state.elementType = elementType
      state.elementId = elementId
      state.elementAction = elementAction
      state.element = null
      state.parent = null
      state.errors = {}
    },
    fetchElementSuccess: setElements,
    fetchElementError: setErrors,
    storeElementInit: resetElementErrors,
    storeElementSuccess: setElement,
    storeElementError: setElementErrors,
    patchElementInit: resetElementErrors,
    patchElementSuccess: setElement,
    patchElementError: setElementErrors,
    toggleElementSiteInit: resetElementErrors,
    toggleElementSiteSuccess: setElement,
    toggleElementSiteError: setElementErrors,
    createElementInit(state, action) {
      state.elementType = action.payload
      state.elementId = null
      state.elementAction = 'create'
      state.element = null
      state.parent = null
      state.errors = {}
    },
    createElementSuccess: setElements,
    createElementError: setErrors,
    deleteElementInit: keepState,
    deleteElementSuccess: keepState,
    deleteElementError(state, action) {
      state.errors = action.payload.error.errors
    },
    updateElement(state, action) {
      const { element, values } = action.payload
      state.element = { ...element, ...values }
    }
  }
})

export const actions = elementsSlice.actions

export default elementsSlice.reducer
