import isNil from 'lodash/isNil'

import ManagementApi from '../api/ManagementApi'

import * as actionTypes from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

import { fetchElements, fetchElement } from './elementActions'


// upload file

export function uploadFile(file) {
  const pendingId = 'uploadFile'

  return function(dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(uploadFileInit(file))

    return ManagementApi.uploadFile(file)
      .then(elements => dispatch(uploadFileSuccess(elements)))
      .catch(error => dispatch(uploadFileError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function uploadFileInit(file) {
  return {type: actionTypes.UPLOAD_IMPORT_FILE_INIT, file: file}
}

export function uploadFileSuccess(elements) {
  return {type: actionTypes.UPLOAD_IMPORT_FILE_SUCCESS, elements}
}

export function uploadFileError(error) {
  return {type: actionTypes.UPLOAD_IMPORT_FILE_ERROR, error}
}

// import elements

export function importElements() {
  const pendingId = 'uploadFile'

  return function(dispatch, getState) {
    const elements = getState().imports.elements.filter(element => element.import)

    dispatch(addToPending(pendingId))
    dispatch(importElementsInit())

    return ManagementApi.importElements(elements)
      .then(elements => dispatch(importElementsSuccess(elements)))
      .catch(error => dispatch(importElementsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function importElementsInit() {
  return {type: actionTypes.IMPORT_ELEMENTS_INIT}
}

export function importElementsSuccess(elements) {
  return {type: actionTypes.IMPORT_ELEMENTS_SUCCESS, elements}
}

export function importElementsError(error) {
  return {type: actionTypes.IMPORT_ELEMENTS_ERROR, error}
}

// update elements

export function updateElement(element, values) {
  return {type: actionTypes.UPDATE_IMPORT_ELEMENT, element, values}
}

export function selectElements(value) {
  return {type: actionTypes.SELECT_IMPORT_ELEMENTS, value}
}
export function selectChangedElements(value) {
  return {type: actionTypes.SELECT_CHANGED_IMPORT_ELEMENTS, value}
}

export function showElements(value) {
  return {type: actionTypes.SHOW_IMPORT_ELEMENTS, value}
}
export function showChangedElements(value) {
  return {type: actionTypes.SHOW_CHANGED_IMPORT_ELEMENTS, value}
}

export function updateUriPrefix(uriPrefix) {
  return {type: actionTypes.UPDATE_IMPORT_URI_PREFIX, uriPrefix}
}

export function resetElements() {
  return function(dispatch, getState) {
    const { elementType, elementId, elementAction} = getState().elements
    if (isNil(elementId)) {
      dispatch(fetchElements(elementType, elementAction))
    } else {
      dispatch(fetchElement(elementType, elementId, elementAction))
    }
    dispatch({type: actionTypes.RESET_IMPORT_ELEMENTS})
  }
}
