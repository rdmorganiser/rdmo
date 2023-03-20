import ls from 'local-storage'

import { lsKeys } from '../constants/config'

const initialState = {
  baseUrl: '/management/',
  filterUri: '',
  filterUriPrefix: ''
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case 'config/updateConfig':
      const newState = {...state, ...{ settings: action.config }}

      // store the new state in the local storage
      lsKeys.forEach(key => ls.set(`rdmo.management.config.${key}`, newState[key]))

      // return the new state
      return newState
    case 'config/fetchSettingsSuccess':
      return {...state, ...{ settings: action.settings }}
    case 'config/fetchMetaSuccess':
      return {...state, ...{ meta: action.meta }}
    case 'elements/fetchElementsInit':
    case 'elements/fetchElementInit':
    case 'elements/storeElementInit':
    case 'elements/createElementInit':
    case 'elements/deleteElementInit':
      return {...state, ...{ pending: true }}
    case 'elements/fetchElementsSuccess':
    case 'elements/fetchElementsError':
    case 'elements/fetchElementSuccess':
    case 'elements/fetchElementError':
    case 'elements/storeElementSuccess':
    case 'elements/storeElementError':
    case 'elements/createElementSuccess':
    case 'elements/createElementError':
    case 'elements/deleteElementSuccess':
    case 'elements/deleteElementError':
      return {...state, ...{ pending: false }}
    default:
      return state
  }
}
