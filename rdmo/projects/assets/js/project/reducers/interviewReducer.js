import { isNil } from 'lodash'

import * as actionTypes from '../actions/actionTypes'
import { sortValues } from '../utils/value'

const initialState = {
  done: null,
  page: null,
  navigation: null,
  values: null,
  attributes: [],
  sets: [],
  errors: []
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case actionTypes.FETCH_PAGE_SUCCESS:
      return { ...state, page: action.page, done: action.done }
    case actionTypes.FETCH_VALUES_SUCCESS:
      return { ...state, values: action.values, sets: action.sets }
    case actionTypes.FETCH_OPTIONS_SUCCESS:
      return { ...state, page: action.page }
    case actionTypes.RESOLVE_CONDITIONS_SUCCESS:
      return {
        ...state, sets: state.sets.map(
          (set) => {
          // filter all results for the current set
            const results = action.results.filter((result) => (
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
          }
        )
      }
    case actionTypes.CREATE_VALUE:
      return { ...state, values: [...state.values, action.value] }
    case actionTypes.UPDATE_VALUE:
      return {
        ...state,
        values: state.values.map(
          (value) => value.id == action.value.id ? {...value, ...action.attrs} : value
        )
      }
    case actionTypes.STORE_VALUE_SUCCESS:
      if (state.values.some((value) => (value.id || value.tmp_id) == action.valueId)) {
        return {
          ...state,
          values: state.values.map((value) => (
            (value.id || value.tmp_id) == action.valueId ? action.value : value
          ))
        }
      } else {
        return { ...state, values: [...state.values, action.value] }
      }
    case actionTypes.DELETE_VALUE_SUCCESS:
      return {
        ...state,
        values: state.values.filter((value) => (
          (value.id || value.tmp_id) != action.valueId
        ))
      }
    case actionTypes.CREATE_SET:
      return { ...state, values: action.values, sets: action.sets }
    case actionTypes.DELETE_SET_SUCCESS:
      return {
        ...state,
        values: state.values.filter((value) => !action.values.includes(value)),
        sets: state.sets.filter((set) => !action.sets.includes(set))
      }
    case actionTypes.COPY_SET_SUCCESS:
      return { ...state, values: action.values, sets: action.sets }
    case actionTypes.FETCH_PAGE_INIT:
    case actionTypes.FETCH_OPTIONS_INIT:
    case actionTypes.FETCH_VALUES_INIT:
    case actionTypes.RESOLVE_CONDITIONS_INIT:
      return { ...state, errors: [] }
    case actionTypes.STORE_VALUE_INIT:
      return {
        ...state,
        values: state.values.map((value) => (
          (value.id || value.tmp_id) == action.valueId ? {...value, error: null, pending: true} : value
        ))
      }
    case actionTypes.DELETE_VALUE_INIT:
      return {
        ...state,
        values: state.values.map((value) => (
          (value.id || value.tmp_id) == action.valueId ? {...value, pending: true} : value
        ))
      }
    case actionTypes.DELETE_SET_INIT:
    case actionTypes.COPY_SET_INIT:
      return { ...state, errors: [] }
    case actionTypes.FETCH_PAGE_ERROR:
    case actionTypes.FETCH_OPTIONS_ERROR:
    case actionTypes.FETCH_VALUES_ERROR:
    case actionTypes.RESOLVE_CONDITIONS_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case actionTypes.STORE_VALUE_ERROR:
      if (!isNil(action.valueId)) {
        return {
          ...state,
          values: state.values.map((value) => (
            (value.id || value.tmp_id) == action.valueId ? {...value, error: action.error, pending: false} : value
          ))
        }
      } else {
        return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
      }
    case actionTypes.DELETE_VALUE_ERROR:
    case actionTypes.DELETE_SET_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case actionTypes.COPY_SET_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case actionTypes.RESORT_VALUES:
      return { ...state, values: sortValues(state.values) }
    default:
      return state
  }
}
