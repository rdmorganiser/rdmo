import { DELETE_CONFIG, UPDATE_CONFIG } from './types'

export function updateConfig(path, value) {
  return {type: UPDATE_CONFIG, path, value}
}

export function deleteConfig(path) {
  return {type: DELETE_CONFIG, path}
}
