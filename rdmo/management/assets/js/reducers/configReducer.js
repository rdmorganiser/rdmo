import set from 'lodash/set'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

const initialState = {
  baseUrl: baseUrl + '/management/',
  apiUrl: baseUrl + '/api/v1/',
  settings: {},
  filter: {},
  display: {}
}

export default function configReducer(state = initialState, action) {
  let newState
  switch(action.type) {
    case 'config/updateConfig':
      newState = {...state}

      set(newState, action.path, action.value)
      localStorage.setItem(`rdmo.management.config.${action.path}`, action.value)

      return newState
    case 'config/fetchConfigSuccess':
      return {...state, ...action.config, currentSite: action.config.sites.find(site => site.current)}
    default:
      return state
  }
}
