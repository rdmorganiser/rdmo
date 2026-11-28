import * as errorActions from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

import { actions } from '../reducers/exportSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchExports() {
  return function (dispatch) {
    dispatch(addToPending('fetchExports'))
    dispatch(errorActions.clearError('exports'))
    dispatch(actions.fetchExportsInit())

    return ProjectApi.fetchExports()
      .then(exportList => dispatch(actions.fetchExportsSuccess(exportList)))
      .catch(error => dispatch(errorActions.setError('exports', error, gettext('Exports'))))
      .finally(() => dispatch(removeFromPending('fetchExports')))
  }
}

export function fetchExport(key) {
  return function (dispatch) {
    dispatch(addToPending('fetchExport'))
    dispatch(errorActions.clearError('export'))
    dispatch(actions.fetchExportInit())

    return ProjectApi.fetchProjectExport(projectId, key)
      .then(response => {
        if (response?.redirect_url) {
          window.location.href = response.redirect_url
        }

        dispatch(actions.fetchExportSuccess({ key, ...response }))
      })
      .catch(error => dispatch(errorActions.setError('export', error, gettext('Export'))))
      .finally(() => dispatch(removeFromPending('fetchExport')))
  }
}

export function downloadExport(key) {
  return function (dispatch) {
    dispatch(addToPending('downloadExport'))
    dispatch(errorActions.clearError('export'))
    dispatch(actions.downloadExportInit())

    return ProjectApi.downloadProjectExport(projectId, key)
      .then(() => dispatch(actions.downloadExportSuccess()))
      .catch(error => dispatch(errorActions.setError('export', error, gettext('Export'))))
      .finally(() => dispatch(removeFromPending('downloadExport')))
  }
}

export function submitExport(key, formData) {
  return function (dispatch) {
    dispatch(addToPending('submitExport'))
    dispatch(errorActions.clearError('export'))
    dispatch(actions.submitExportInit())

    return ProjectApi.submitProjectExport(projectId, key, formData)
      .then(response => {
        if (response?.redirect_url) {
          window.location.href = response.redirect_url
        }

        dispatch(actions.submitExportSuccess({ key, ...response }))
        return response
      })
      .catch(error => dispatch(errorActions.setError('export', error, gettext('Export'))))
      .finally(() => dispatch(removeFromPending('submitExport')))
  }
}
