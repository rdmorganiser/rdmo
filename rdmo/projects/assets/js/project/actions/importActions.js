import * as actionTypes from './actionTypes'

export function uploadFileInit(file) {
  return { type: actionTypes.UPLOAD_IMPORT_FILE_INIT, file }
}

export function uploadFileSuccess(values) {
  return { type: actionTypes.UPLOAD_IMPORT_FILE_SUCCESS, values }
}

export function uploadFileError(error) {
  return { type: actionTypes.UPLOAD_IMPORT_FILE_ERROR, error }
}

export function updateValue(value, values) {
  return {
    type: actionTypes.UPDATE_IMPORT_VALUE,
    value,
    values
  }
}

export function selectValues(value) {
  return { type: actionTypes.SELECT_IMPORT_VALUES, value }
}

export function selectChangedValues(value) {
  return { type: actionTypes.SELECT_CHANGED_IMPORT_VALUES, value }
}

export function showValues(value) {
  return { type: actionTypes.SHOW_IMPORT_VALUES, value }
}

export function showChangedValues(value) {
  return { type: actionTypes.SHOW_CHANGED_IMPORT_VALUES, value }
}

export function resetValues() {
  return { type: actionTypes.RESET_IMPORT_VALUES }
}
