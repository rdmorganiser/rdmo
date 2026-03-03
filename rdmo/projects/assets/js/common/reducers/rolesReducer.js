import { FETCH_ROLES_ERROR, FETCH_ROLES_INIT, FETCH_ROLES_SUCCESS } from '../actions/actionTypes'

const initialState = {
  roles: [],
  errors: null,
}

export default function rolesReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_ROLES_INIT:
      return { ...state, errors: null }
    case FETCH_ROLES_SUCCESS:
      return { ...state, roles: action.roles }
    case FETCH_ROLES_ERROR:
      return { ...state, errors: action.error.errors }
    default:
      return state
  }
}
