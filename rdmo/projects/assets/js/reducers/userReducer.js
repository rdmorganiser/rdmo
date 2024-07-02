import { FETCH_CURRENT_USER_ERROR, FETCH_CURRENT_USER_INIT, FETCH_CURRENT_USER_SUCCESS }
  from '../actions/actionTypes'

const initialState = {
  currentUser: {},
}

export default function userReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_CURRENT_USER_INIT:
      return {...state, ...action.currentUser}
    case FETCH_CURRENT_USER_SUCCESS:
      return {...state, ...action.currentUser}
    case FETCH_CURRENT_USER_ERROR:
      return {...state, errors: action.error.errors}
    default:
       return state
  }
}
