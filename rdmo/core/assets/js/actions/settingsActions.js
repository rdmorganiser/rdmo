import { actions } from '../reducers/settingsSlice'

import CoreApi from '../api/CoreApi'

import * as errorActions from './errorsActions'

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
  return errorActions.setError('settings', errors, gettext('Settings'))
}
