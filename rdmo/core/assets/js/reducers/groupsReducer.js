import { FETCH_GROUPS_ERROR, FETCH_GROUPS_SUCCESS } from '../actions/actionTypes'

const initialState = {}

export default function groupsReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_GROUPS_SUCCESS:
      return { ...state, ...action.groups }
    case FETCH_GROUPS_ERROR:
      return { ...state, errors: action.error }
    default:
      return state
  }
}
