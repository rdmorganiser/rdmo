import { actions } from '../reducers/configSlice'

export function updateConfig(path, value) {
  return actions.updateConfig({ path, value })
}

export function deleteConfig(path) {
  return actions.deleteConfig({ path })
}
