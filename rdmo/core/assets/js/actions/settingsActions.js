import CoreApi from '../api/CoreApi'

import { FETCH_SETTINGS_ERROR, FETCH_SETTINGS_INIT, FETCH_SETTINGS_SUCCESS } from './actionTypes'

export function fetchSettings() {
  return function(dispatch) {
    dispatch(fetchSettingsInit())

    return CoreApi.fetchSettings()
      .then((settings) => dispatch(fetchSettingsSuccess(settings)))
      .catch((errors) => dispatch(fetchSettingsError(errors)))
  }
}

export function fetchSettingsInit() {
  return {type: FETCH_SETTINGS_INIT}
}

export function fetchSettingsSuccess(settings) {
  return {type: FETCH_SETTINGS_SUCCESS, settings}
}

export function fetchSettingsError(errors) {
  return {type: FETCH_SETTINGS_ERROR, errors}
}
