import { processElementDiffs } from 'rdmo/management/assets/js/utils/diff'

import * as actionTypes from '../actions/actionTypes'

const initialState = {
  errors: [],
  file: null,
  values: []
}

export default function projectImportReducer(state = initialState, action) {
  switch (action.type) {
    case actionTypes.UPLOAD_IMPORT_FILE_INIT:
      return { ...initialState, file: action.file }
    case actionTypes.UPLOAD_IMPORT_FILE_SUCCESS:
      return {
        ...state,
        values: action.values.map(value => ({
          ...processElementDiffs(value),
          import: value.errors.length === 0,
          show: false
        }))
      }
    case actionTypes.UPLOAD_IMPORT_FILE_ERROR:
      return { ...state, errors: action.error.errors }
    case actionTypes.UPDATE_IMPORT_VALUE:
      return {
        ...state,
        values: state.values.map(value => (
          value === action.value ? { ...value, ...action.values } : value
        ))
      }
    case actionTypes.SELECT_IMPORT_VALUES:
      return {
        ...state,
        values: state.values.map(value => ({
          ...value,
          import: value.errors.length === 0 && action.value
        }))
      }
    case actionTypes.SELECT_CHANGED_IMPORT_VALUES:
      return {
        ...state,
        values: state.values.map(value => {
          if (value.changed || value.created) {
            return {
              ...value,
              import: value.errors.length === 0 && action.value
            }
          } else if (action.value) {
            return { ...value, import: false }
          } else {
            return value
          }
        })
      }
    case actionTypes.SHOW_IMPORT_VALUES:
      return {
        ...state,
        values: state.values.map(value => ({ ...value, show: action.value }))
      }
    case actionTypes.SHOW_CHANGED_IMPORT_VALUES:
      return {
        ...state,
        values: state.values.map(value => {
          if (value.changed || value.created) {
            return { ...value, show: action.value }
          } else if (action.value) {
            return { ...value, show: false }
          } else {
            return value
          }
        })
      }
    case actionTypes.RESET_IMPORT_VALUES:
      return { ...state, values: [] }
    default:
      return state
  }
}
