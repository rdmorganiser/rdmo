import { actions } from '../reducers/configSlice'

export function updateConfig(path, value, ls = true) {
  return actions.updateConfig({ path, value, ls })
}

export function deleteConfig(path, ls = true) {
  return actions.deleteConfig({ path, ls })
}
