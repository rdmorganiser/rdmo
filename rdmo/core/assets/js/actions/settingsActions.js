import { actions as errorActions } from '../reducers/errorsSlice'
import { actions } from '../reducers/settingsSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

export function fetchSettings() {
  return function(dispatch) {
    dispatch(fetchSettingsInit())

    return CoreApi.fetchSettings()
      .then((settings) => dispatch(fetchSettingsSuccess(settings)))
      .catch((errors) => dispatch(fetchSettingsError(errors)))
  }
}

export function fetchSettingsInit() {
  return errorActions.clearError('settings')
}

export function fetchSettingsSuccess(settings) {
  return actions.fetchSettingsSuccess(settings)
}

export function fetchSettingsError(errors) {
  return errorActions.setError({
    source: 'settings',
    error: { ...serializeError(errors), context: gettext('Settings') }
  })
}
