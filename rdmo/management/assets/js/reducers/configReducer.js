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
      return {...state, ...{ pending: true }}
    case 'elements/fetchElementsSuccess':
      return {...state, ...{ pending: false }}
    case 'elements/fetchElementsError':
      return {...state, ...{ pending: false }}
    case 'elements/fetchElementInit':
      return {...state, ...{ pending: true }}
    case 'elements/fetchElementSuccess':
      return {...state, ...{ pending: false }}
    case 'elements/fetchElementError':
      return {...state, ...{ pending: false }}
    case 'elements/storeElementInit':
      return {...state, ...{ pending: true }}
    case 'elements/storeElementSuccess':
      return {...state, ...{ pending: false }}
    case 'elements/storeElementError':
      return {...state, ...{ pending: false }}
    case 'elements/deleteElementInit':
      return {...state, ...{ pending: true }}
    case 'elements/deleteElementSuccess':
      return {...state, ...{ pending: false }}
    case 'elements/deleteElementError':
      return {...state, ...{ pending: false }}
    default:
      return state
  }
}
