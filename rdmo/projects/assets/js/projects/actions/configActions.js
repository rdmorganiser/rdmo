import { DELETE_CONFIG, UPDATE_CONFIG } from './actionTypes'

export function updateConfig(path, value) {
  return {type: UPDATE_CONFIG, path, value}
}

export function deleteConfig(path) {
  return {type: DELETE_CONFIG, path}
}
