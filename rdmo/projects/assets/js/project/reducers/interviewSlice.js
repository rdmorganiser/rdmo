import { createSlice, original } from '@reduxjs/toolkit'
import { pick } from 'lodash'

import { compareValueId, sortValues } from '../utils/value'

const initialState = {
  done: false,
  page: null,
  continuation: null,
  providerOptions: {},
  navigation: null,
  values: null,
  valuesRequestId: null,
  attributes: [],
  sets: []
}

const setValues = (state, action) => {
  state.values = action.payload.values
  state.sets = action.payload.sets
}

const keepState = state => state

const interviewSlice = createSlice({
  name: 'interview',
  initialState,
  reducers: {
    fetchPageInit(state) {
      state.done = false
    },
    fetchPageSuccess(state, action) {
      state.page = action.payload.page
      state.providerOptions = {}
      state.values = null
      state.sets = []
    },
    fetchContinueSuccess(state, action) {
      state.continuation = action.payload
    },
    fetchValuesInit(state, action) {
      state.valuesRequestId = action.payload
    },
    fetchValuesSuccess: setValues,
    fetchOptionsSuccess(state, action) {
      const { pageId, optionsetId, options } = action.payload
      if (state.page?.id === pageId) {
        state.providerOptions[optionsetId] = options
      }
    },
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
    createValue(state, action) {
      state.values.push(action.payload)
    },
    updateValue(state, action) {
      const { value, attrs, store = false } = action.payload
      state.values = state.values.map(currentValue => (
        compareValueId(currentValue, value.id || value.tmp_id) ? {
          ...currentValue,
          ...attrs,
          revision: (currentValue.revision || 0) + (store ? 1 : 0),
          success: store ? false : (attrs.success ?? currentValue.success)
        } : currentValue
      ))
    },
    storeValueInit(state, action) {
      state.values = state.values.map(value => (
        compareValueId(value, action.payload) ? { ...value, error: null, pending: true } : value
      ))
    },
    storeValueMetadata(state, action) {
      const { value, valueId } = action.payload
      state.values = state.values.map(currentValue => (
        compareValueId(currentValue, valueId) ? {
          ...currentValue, ...pick(value, ['id', 'created', 'updated'])
        } : currentValue
      ))
    },
    storeValueSuccess(state, action) {
      const { value, valueId, revision = 0 } = action.payload
      if (state.values.some(currentValue => compareValueId(currentValue, valueId))) {
        state.values = state.values.map(currentValue => {
          if (!compareValueId(currentValue, valueId)) return currentValue
          const pending = (currentValue.revision || 0) !== revision
          // An older response acknowledges the save without replacing newer input.
          const attrs = pending ? pick(value, ['id', 'created', 'updated', 'file_name', 'file_url']) : value
          return { ...currentValue, ...attrs, savedRevision: revision, error: null, pending }
        })
      } else {
        state.values.push(value)
      }
    },
    storeValueError(state, action) {
      const { error, valueId } = action.payload
      state.values = state.values.map(value => (
        compareValueId(value, valueId) ? { ...value, error, pending: false } : value
      ))
    },
    deleteValueInit(state, action) {
      state.values = state.values.map(value => (
        compareValueId(value, action.payload) ? { ...value, error: null, pending: true } : value
      ))
    },
    deleteValueSuccess(state, action) {
      state.values = state.values.filter(value => !compareValueId(value, action.payload))
    },
    deleteValueError(state, action) {
      const { error, valueId } = action.payload
      state.values = state.values.map(value => (
        compareValueId(value, valueId) ? { ...value, error, pending: false } : value
      ))
    },
    createSet: setValues,
    deleteSetSuccess(state, action) {
      const { values, sets } = action.payload
      state.values = original(state.values).filter(value => !values.includes(value))
      state.sets = original(state.sets).filter(set => !sets.includes(set))
    },
    copySetSuccess: setValues,
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
