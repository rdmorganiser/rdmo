import { DELETE_CONFIG, UPDATE_CONFIG } from '../actions/actionTypes'
import { deleteConfig, deleteConfigInLocalStorage, setConfigInLocalStorage, updateConfig } from '../utils/config'

const initialState = {}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case UPDATE_CONFIG:
      if (action.ls) {
        setConfigInLocalStorage(state.prefix, action.path, action.value)
      }
      return updateConfig(state, action.path, action.value)
    case DELETE_CONFIG:
      if (action.ls) {
        deleteConfigInLocalStorage(state.prefix, action.path)
      }
      return deleteConfig(state, action.path)
    default:
      return state
  }
}
