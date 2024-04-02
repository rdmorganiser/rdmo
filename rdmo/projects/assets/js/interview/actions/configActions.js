import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

import { FETCH_CONFIG_SUCCESS, FETCH_CONFIG_ERROR, UPDATE_CONFIG } from './types'

export function fetchConfig() {
  return (dispatch) => Promise.all([
    CoreApi.fetchSettings(),
    CoreApi.fetchTemplates(),
  ]).then(([settings, templates]) => dispatch(fetchConfigSuccess({
    settings, templates
  })))
}

export function fetchConfigSuccess(config) {
  return {type: FETCH_CONFIG_SUCCESS, config}
}

export function fetchConfigError(errors) {
  return {type: FETCH_CONFIG_ERROR, errors}
}

export function updateConfig(path, value) {
  return {type: UPDATE_CONFIG, path, value}
}
