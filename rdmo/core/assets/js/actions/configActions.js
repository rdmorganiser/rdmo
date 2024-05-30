import { setConfigInLocalStorage, deleteConfigInLocalStorage } from '../utils/config'

import { UPDATE_CONFIG, DELETE_CONFIG } from './actionTypes'

export function updateConfig(prefix, path, value) {
  setConfigInLocalStorage(prefix, path, value)
  return {type: UPDATE_CONFIG, path, value}
}

export function deleteConfig(prefix, path) {
  deleteConfigInLocalStorage(prefix, path)
  return {type: DELETE_CONFIG, path}
}
