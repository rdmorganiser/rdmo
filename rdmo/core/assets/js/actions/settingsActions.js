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
  return actions.fetchSettingsInit()
}

export function fetchSettingsSuccess(settings) {
  return actions.fetchSettingsSuccess(settings)
}

export function fetchSettingsError(errors) {
  return actions.fetchSettingsError(serializeError(errors))
}
