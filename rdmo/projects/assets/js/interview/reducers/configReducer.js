import set from 'lodash/set'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

import { FETCH_CONFIG_SUCCESS, FETCH_CONFIG_ERROR, UPDATE_CONFIG } from '../actions/types'

const initialState = {
  baseUrl: baseUrl + '/interview/',
  settings: {}
}

export default function configReducer(state = initialState, action) {
  let newState
  switch(action.type) {
    case UPDATE_CONFIG:
      newState = {...state}

      set(newState, action.path, action.value)
      localStorage.setItem(`rdmo.management.config.${action.path}`, action.value)

      return newState
    case FETCH_CONFIG_SUCCESS:
      return {...state, ...action.config}
    case FETCH_CONFIG_ERROR:
      return {...state, pending: false }
    default:
      return state
  }
}
