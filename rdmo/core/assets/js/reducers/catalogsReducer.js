import { FETCH_CATALOGS_ERROR, FETCH_CATALOGS_INIT, FETCH_CATALOGS_SUCCESS } from '../actions/actionTypes'

const initialState = {}

export default function settingsReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_CATALOGS_INIT:
        return {...state, ...action.catalogs}
    case FETCH_CATALOGS_SUCCESS:
      return {...state, ...action.catalogs}
    case FETCH_CATALOGS_ERROR:
      return {...state, errors: action.error.errors}
    default:
      return state
  }
}
