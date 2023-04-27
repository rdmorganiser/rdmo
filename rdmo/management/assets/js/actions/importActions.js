import ManagementApi from '../api/ManagementApi'

// upload file

export function uploadFile(file) {
  return function(dispatch) {
    dispatch(uploadFileInit())

    return ManagementApi.uploadFile(file)
      .then(elements => dispatch(uploadFileSuccess(elements)))
      .catch(error => dispatch(uploadFileError([error.message])))
  }
}

export function uploadFileInit() {
  return {type: 'import/uploadFileInit'}
}

export function uploadFileSuccess(elements) {
  return {type: 'import/uploadFileSuccess', elements}
}

export function uploadFileError(errors) {
  return {type: 'import/uploadFileError', errors}
}

// import elements

export function importElements() {
  return function(dispatch, getState) {
    const elements = getState().imports.elements.filter(element => element.import)

    dispatch(importElementsInit())

    return ManagementApi.importElements(elements)
      .then(elements => dispatch(importElementsSuccess(elements)))
      .catch(error => dispatch(importElementsError([error.message])))
  }
}

export function importElementsInit() {
  return {type: 'import/importElementsInit'}
}

export function importElementsSuccess(elements) {
  return {type: 'import/importElementsSuccess', elements}
}

export function importElementsError(errors) {
  return {type: 'import/importElementsError', errors}
}

// update elements

export function updateElement(element, values) {
  return {type: 'import/updateElement', element, values}
}

export function updateElements(values) {
  return {type: 'import/updateElements', values}
}
