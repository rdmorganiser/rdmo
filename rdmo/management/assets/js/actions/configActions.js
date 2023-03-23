import CoreApi from 'rdmo/core/assets/js/api/CoreApi'
import ManagementApi from '../api/ManagementApi'

export function updateConfig(path, value) {
  return {type: 'config/updateConfig', path, value}
}

export function fetchSettings() {
  return function(dispatch) {
    return CoreApi.fetchSettings()
      .then(settings => dispatch(fetchSettingsSuccess(settings)))
      .catch(error => dispatch(fetchSettingsError([error.message])))
  }
}

export function fetchSettingsSuccess(settings) {
  return {type: 'config/fetchSettingsSuccess', settings}
}

export function fetchSettingsError(errors) {
  return {type: 'elements/fetchSettingsError', errors}
}

export function fetchMeta() {
  return function(dispatch) {
    return ManagementApi.fetchMeta()
      .then(meta => dispatch(fetchMetaSuccess(meta)))
      .catch(error => dispatch(fetchMetaError([error.message])))
  }
}

export function fetchMetaSuccess(meta) {
  return {type: 'config/fetchMetaSuccess', meta}
}

export function fetchMetaError(errors) {
  return {type: 'elements/fetchMetaError', errors}
}
