import { actions } from '../reducers/configSlice'
import { deleteConfigInLocalStorage, setConfigInLocalStorage } from '../utils/config'

export function updateConfig(path, value) {
  return (dispatch, getState) => {
    setConfigInLocalStorage(getState().config.prefix, path, value)
    dispatch(actions.updateConfig({ path, value }))
  }
}

export function deleteConfig(path) {
  return (dispatch, getState) => {
    deleteConfigInLocalStorage(getState().config.prefix, path)
    dispatch(actions.deleteConfig({ path }))
  }
}
