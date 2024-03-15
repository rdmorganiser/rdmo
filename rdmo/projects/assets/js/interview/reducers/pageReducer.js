import { FETCH_PAGE_SUCCESS, FETCH_PAGE_ERROR } from '../actions/types'

const initialState = {
  display: false
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_PAGE_SUCCESS:
      return {...state, ...action.page, display: true}
    case FETCH_PAGE_ERROR:
      return {...state }
    default:
      return state
  }
}
