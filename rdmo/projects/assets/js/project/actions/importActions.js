import * as errorActions from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/importSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchImports() {
  return function (dispatch) {
    dispatch(addToPending('fetchImports'))
    dispatch(errorActions.clearError('imports'))
    dispatch(actions.fetchImportsInit())

    return ProjectApi.fetchImports()
      .then(importList => dispatch(actions.fetchImportsSuccess(importList)))
      .catch(error => dispatch(errorActions.setError('imports', error, gettext('Imports'))))
      .finally(() => dispatch(removeFromPending('fetchImports')))
  }
}

export function uploadImport(file) {
  return function (dispatch) {
    dispatch(addToPending('uploadImport'))
    dispatch(actions.uploadImportInit())

    return ProjectApi.uploadProjectImport(projectId, file)
      .then(response => {
        dispatch(actions.uploadImportSuccess())
        return response
      })
      .catch(error => dispatch(actions.uploadImportError(serializeError(error))))
      .finally(() => dispatch(removeFromPending('uploadImport')))
  }
}

export function fetchImport(key) {
  return function (dispatch) {
    dispatch(addToPending('fetchImport'))
    dispatch(errorActions.clearError('import'))
    dispatch(actions.fetchImportInit())

    return ProjectApi.fetchProjectImport(projectId, key)
      .then(response => dispatch(actions.fetchImportSuccess({ key, ...response })))
      .catch(error => dispatch(errorActions.setError('import', error, gettext('Import'))))
      .finally(() => dispatch(removeFromPending('fetchImport')))
  }
}

export function submitImport(key, formData) {
  return function (dispatch) {
    dispatch(addToPending('submitImport'))
    dispatch(errorActions.clearError('import'))
    dispatch(actions.submitImportInit())

    return ProjectApi.submitProjectImport(projectId, key, formData)
      .then(response => {
        dispatch(actions.submitImportSuccess({ key, ...response }))
        return response
      })
      .catch(error => dispatch(errorActions.setError('import', error, gettext('Import'))))
      .finally(() => dispatch(removeFromPending('submitImport')))
  }
}
