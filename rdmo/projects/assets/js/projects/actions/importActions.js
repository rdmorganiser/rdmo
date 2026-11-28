import { isNil } from 'lodash'

import * as errorActions from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/importSlice'
import { updateLocation } from '../utils/location'

import ProjectsApi from '../api/ProjectsApi'

export function navigateImport(importKey) {
  return function (dispatch) {
    updateLocation({ importKey })
    dispatch(actions.setImportKey(importKey))

    if (!isNil(importKey)) {
      dispatch(fetchImport(importKey))
    }
  }
}

export function fetchImports() {
  return function (dispatch) {
    dispatch(addToPending('fetchImports'))
    dispatch(errorActions.clearError('imports'))
    dispatch(actions.fetchImportsInit())

    return ProjectsApi.fetchImports()
      .then(importList => dispatch(actions.fetchImportsSuccess(importList)))
      .catch(error => dispatch(errorActions.setError('imports', error, gettext('Imports'))))
      .finally(() => dispatch(removeFromPending('fetchImports')))
  }
}

export function uploadImport(file) {
  return function (dispatch) {
    dispatch(addToPending('uploadImport'))
    dispatch(actions.uploadImportInit())

    return ProjectsApi.uploadImport(file)
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

    return ProjectsApi.fetchImport(key)
      .then(response => {
        if (response?.redirect_url) {
          window.location.href = response.redirect_url
        }

        dispatch(actions.fetchImportSuccess({ key, ...response }))
      })
      .catch(error => dispatch(errorActions.setError('import', error, gettext('Import'))))
      .finally(() => dispatch(removeFromPending('fetchImport')))
  }
}

export function submitImport(key, formData) {
  return function (dispatch) {
    dispatch(addToPending('submitImport'))
    dispatch(errorActions.clearError('import'))
    dispatch(actions.submitImportInit())

    return ProjectsApi.submitImport(key, formData)
      .then(response => {
        if (response?.redirect_url) {
          window.location.href = response.redirect_url
        }

        dispatch(actions.submitImportSuccess({ key, ...response }))
        return response
      })
      .catch(error => dispatch(errorActions.setError('import', error, gettext('Import'))))
      .finally(() => dispatch(removeFromPending('submitImport')))
  }
}

export function clearUploadError() {
  return actions.clearUploadError()
}
