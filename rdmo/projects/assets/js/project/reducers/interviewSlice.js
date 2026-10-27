import { isNil } from 'lodash'

import { sortValues } from '../utils/value'

import { createSlice, original } from '@reduxjs/toolkit'

const initialState = {
  done: false,
  page: null,
  continuation: null,
  navigation: null,
  values: null,
  attributes: [],
  sets: [],
  errors: []
}

const clearErrors = state => {
  state.errors = []
}

const appendError = (state, action) => {
  state.errors.push({ actionType: action.type, ...action.payload })
}

const setValues = (state, action) => {
  state.values = action.payload.values
  state.sets = action.payload.sets
}

const matchesValueId = (value, valueId) => (value.id || value.tmp_id) == valueId

const keepState = state => state

const interviewSlice = createSlice({
  name: 'interview',
  initialState,
  reducers: {
    fetchPageInit(state) {
      clearErrors(state)
      state.done = false
    },
    fetchPageSuccess(state, action) {
      state.page = action.payload.page
    },
    fetchPageError: appendError,
    fetchContinueInit: clearErrors,
    fetchContinueSuccess(state, action) {
      state.continuation = action.payload
    },
    fetchContinueError: appendError,
    fetchValuesInit: clearErrors,
    fetchValuesSuccess: setValues,
    fetchValuesError: appendError,
    fetchOptionsInit: clearErrors,
    fetchOptionsSuccess(state, action) {
      state.page = action.payload
    },
    fetchOptionsError: appendError,
    resolveConditionsInit: clearErrors,
    resolveConditionsSuccess(state, action) {
      state.sets = state.sets.map(set => {
        // filter all results for the current set
        const results = action.payload.filter(result => (
          result.set_prefix === set.set_prefix &&
          result.set_index === set.set_index
        ))

        // apply the results
        return results.reduce((acc, result) => ({
          ...acc,
          [result.element_type]: {
            ...acc[result.element_type],
            [result.element_id]: result.result
          },
        }), set)
      })
    },
    resolveConditionsError: appendError,
    createValue(state, action) {
      state.values.push(action.payload)
    },
    updateValue(state, action) {
      const { value, attrs } = action.payload
      state.values = state.values.map(currentValue => (
        currentValue.id == value.id ? { ...currentValue, ...attrs } : currentValue
      ))
    },
    storeValueInit(state, action) {
      state.values = state.values.map(value => (
        matchesValueId(value, action.payload) ? { ...value, error: null, pending: true } : value
      ))
    },
    storeValueSuccess(state, action) {
      const { value, valueId } = action.payload
      if (state.values.some(currentValue => matchesValueId(currentValue, valueId))) {
        state.values = state.values.map(currentValue => (
          matchesValueId(currentValue, valueId) ? value : currentValue
        ))
      } else {
        state.values.push(value)
      }
    },
    storeValueError(state, action) {
      const { error, valueId } = action.payload
      if (!isNil(valueId)) {
        state.values = state.values.map(value => (
          matchesValueId(value, valueId) ? { ...value, error, pending: false } : value
        ))
      } else {
        appendError(state, { type: action.type, payload: error })
      }
    },
    deleteValueInit(state, action) {
      state.values = state.values.map(value => (
        matchesValueId(value, action.payload) ? { ...value, pending: true } : value
      ))
    },
    deleteValueSuccess(state, action) {
      state.values = state.values.filter(value => !matchesValueId(value, action.payload))
    },
    deleteValueError: appendError,
    createSet: setValues,
    deleteSetInit: clearErrors,
    deleteSetSuccess(state, action) {
      const { values, sets } = action.payload
      state.values = original(state.values).filter(value => !values.includes(value))
      state.sets = original(state.sets).filter(set => !sets.includes(set))
    },
    deleteSetError: appendError,
    copySetInit: clearErrors,
    copySetSuccess: setValues,
    copySetError: appendError,
    resortValues(state) {
      state.values = sortValues(state.values)
    },
    showDone(state) {
      state.done = true
    },
    hideDone(state) {
      state.done = false
    },
    noop: keepState
  }
})

export const actions = interviewSlice.actions

export default interviewSlice.reducer
