import { FETCH_TEMPLATES_ERROR, FETCH_TEMPLATES_SUCCESS } from '../actions/actionTypes'

const initialState = {}

export default function templateReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_TEMPLATES_SUCCESS:
      return { ...state, ...action.templates }
    case FETCH_TEMPLATES_ERROR:
      return { ...state, errors: action.errors }
    default:
      return state
  }
}
