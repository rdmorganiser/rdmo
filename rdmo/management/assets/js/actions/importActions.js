import isNil from 'lodash/isNil'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/importsSlice'

import ManagementApi from '../api/ManagementApi'

import { fetchElement, fetchElements } from './elementActions'


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
  return actions.uploadFileInit(file)
}

export function uploadFileSuccess(elements) {
  return actions.uploadFileSuccess(elements)
}

export function uploadFileError(error) {
  return actions.uploadFileError(serializeError(error))
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
  return actions.importElementsInit()
}

export function importElementsSuccess(elements) {
  return actions.importElementsSuccess(elements)
}

export function importElementsError(error) {
  return actions.importElementsError(serializeError(error))
}

// update elements

export function updateElement(element, values) {
  return actions.updateElement({ element, values })
}

export function selectElements(value) {
  return actions.selectElements(value)
}
export function selectChangedElements(value) {
  return actions.selectChangedElements(value)
}

export function showElements(value) {
  return actions.showElements(value)
}
export function showChangedElements(value) {
  return actions.showChangedElements(value)
}

export function updateUriPrefix(uriPrefix) {
  return actions.updateUriPrefix(uriPrefix)
}

export function resetElements() {
  return function(dispatch, getState) {
    const { elementType, elementId, elementAction} = getState().elements
    if (isNil(elementId)) {
      dispatch(fetchElements(elementType, elementAction))
    } else {
      dispatch(fetchElement(elementType, elementId, elementAction))
    }
    dispatch(actions.resetElements())
  }
}
