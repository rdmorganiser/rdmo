import { updateConfig, deleteConfig } from '../utils/config'

import { DELETE_CONFIG, UPDATE_CONFIG } from '../actions/actionTypes'

const initialState = {}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case UPDATE_CONFIG:
      return updateConfig(state, action.path, action.value)
    case DELETE_CONFIG:
      return deleteConfig(state, action.path)
    default:
      return state
  }
}
