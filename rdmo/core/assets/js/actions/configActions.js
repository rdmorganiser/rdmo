import { UPDATE_CONFIG, DELETE_CONFIG } from './actionTypes'

export function updateConfig(path, value, ls = true) {
  return {type: UPDATE_CONFIG, path, value, ls}
}

export function deleteConfig(path, ls = true) {
  return {type: DELETE_CONFIG, path, ls}
}
