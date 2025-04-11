import { FETCH_SETTINGS_ERROR, FETCH_SETTINGS_SUCCESS } from '../actions/actionTypes'

const initialState = {}

export default function settingsReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_SETTINGS_SUCCESS:
      return { ...state, ...action.settings }
    case FETCH_SETTINGS_ERROR:
      return { ...state, errors: action.errors }
    default:
      return state
  }
}
