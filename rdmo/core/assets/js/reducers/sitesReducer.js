import { FETCH_SITES_ERROR, FETCH_SITES_SUCCESS } from '../actions/actionTypes'

const initialState = {}

export default function sitesReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_SITES_SUCCESS:
      return { ...state, ...action.sites }
    case FETCH_SITES_ERROR:
      return { ...state, errors: action.error }
    default:
      return state
  }
}
