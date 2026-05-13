import {
  FETCH_GROUPS_ERROR,
  FETCH_GROUPS_SUCCESS,
  FETCH_SITES_ERROR,
  FETCH_SITES_SUCCESS
} from '../actions/actionTypes'

const initialState = {}

export function sitesReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_SITES_SUCCESS:
      return { ...state, ...action.sites }
    case FETCH_SITES_ERROR:
      return { ...state, errors: action.error }
    default:
      return state
  }
}

export function groupsReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_GROUPS_SUCCESS:
      return { ...state, ...action.groups }
    case FETCH_GROUPS_ERROR:
      return { ...state, errors: action.error }
    default:
      return state
  }
}
