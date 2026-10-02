import { ADD_TO_STALE, REMOVE_FROM_STALE } from '../actions/actionTypes'

const initialState = {
  items: []
}

export default function staleReducer(state = initialState, action) {
  switch(action.type) {
    case ADD_TO_STALE:
      return { ...state, items: [...new Set([...state.items, action.item])] }
    case REMOVE_FROM_STALE:
      return { ...state, items: state.items.filter((item) => item !== action.item) }
    default:
      return state
  }
}
