import isNil from 'lodash/isNil'

import ManagementApi from '../api/ManagementApi'

import { fetchElements, fetchElement } from './elementActions'

// upload file

export function uploadFile(file) {
  return function(dispatch) {
    dispatch(uploadFileInit())

    return ManagementApi.uploadFile(file)
      .then(elements => dispatch(uploadFileSuccess(elements)))
      .catch(error => {
        dispatch(uploadFileError(error))
      })
  }
}

export function uploadFileInit() {
  return {type: 'import/uploadFileInit'}
}

export function uploadFileSuccess(elements) {
  return {type: 'import/uploadFileSuccess', elements}
}

export function uploadFileError(error) {
  return {type: 'import/uploadFileError', error}
}

// import elements

export function importElements() {
  return function(dispatch, getState) {
    const elements = getState().imports.elements.filter(element => element.import)

    dispatch(importElementsInit())

    return ManagementApi.importElements(elements)
      .then(elements => dispatch(importElementsSuccess(elements)))
      .catch(error => dispatch(importElementsError(error)))
  }
}

export function importElementsInit() {
  return {type: 'import/importElementsInit'}
}

export function importElementsSuccess(elements) {
  return {type: 'import/importElementsSuccess', elements}
}

export function importElementsError(error) {
  return {type: 'import/importElementsError', error}
}

// update elements

export function updateElement(element, values) {
  return {type: 'import/updateElement', element, values}
}

export function selectElements(value) {
  return {type: 'import/selectElements', value}
}

export function updateUriPrefix(uriPrefix) {
  return {type: 'import/updateUriPrefix', uriPrefix}
}

export function resetElements() {
  return function(dispatch, getState) {
    const { elementType, elementId, elementAction} = getState().elements
    if (isNil(elementId)) {
      dispatch(fetchElements(elementType, elementAction))
    } else {
      dispatch(fetchElement(elementType, elementId, elementAction))
    }
    dispatch({type: 'import/resetElements'})
  }
}
