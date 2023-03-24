import ls from 'local-storage'
import set from 'lodash/set'

import { lsKeys } from '../constants/config'

const initialFilter = {
  uri: '',
  uriPrefix: ''
}


const initialState = {
  baseUrl: '/management/',
  filter: {},
  display: {}
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case 'config/updateConfig':
      const newState = {...state}
      const { path, value } = action

      // set the value using lodash's set
      set(newState, path, value)

      // store the new value in the local storage
      if (Object.keys(lsKeys).includes(path)) {
        ls.set(`rdmo.management.config.${path}`, value)
      }

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
