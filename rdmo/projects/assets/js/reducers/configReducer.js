import { set, unset } from 'lodash'
import { DELETE_CONFIG, UPDATE_CONFIG } from '../actions/actionTypes'
import { INITIAL_TABLE_ROWS } from '../utils/constants'

const initialState = {
  myProjects: true,
  params: {},
  showFilters: false,
  tableRows: INITIAL_TABLE_ROWS
}

export default function configReducer(state = initialState, action) {
  let newState
  switch(action.type) {
    case UPDATE_CONFIG:
        newState = {...state}
        set(newState, action.path, action.value)
        localStorage.setItem(`rdmo.projects.config.${action.path}`, action.value.toString())
        return newState
    case DELETE_CONFIG:
      newState = {...state}
      unset(newState, action.path)
      localStorage.removeItem(`rdmo.projects.config.${action.path}`)
      return newState
    default:
       return state
  }
}
