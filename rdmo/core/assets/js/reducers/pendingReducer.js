import { ADD_TO_PENDING, REMOVE_FROM_PENDING } from '../actions/actionTypes'

const initialState = {
  items: []
}

export default function pendingReducer(state = initialState, action) {
  switch(action.type) {
    case ADD_TO_PENDING:
      return { ...state, items: [...state.items, action.item] }
    case REMOVE_FROM_PENDING:
      return { ...state, items: state.items.filter((item) => (item != action.item)) }
    default:
      return state
  }
}
