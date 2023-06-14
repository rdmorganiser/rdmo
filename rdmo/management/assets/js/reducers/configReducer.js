import ls from 'local-storage'
import set from 'lodash/set'

import { lsKeys } from '../constants/config'

const initialState = {
  baseUrl: '/management/',
  settings: {},
  filter: {},
  display: {}
}

export default function configReducer(state = initialState, action) {
  let newState
  switch(action.type) {
    case 'config/updateConfig':
      newState = {...state}

      // set the value using lodash's set
      set(newState, action.path, action.value)

      // store the new value in the local storage
      if (Object.keys(lsKeys).includes(action.path)) {
        ls.set(`rdmo.management.config.${action.path}`, action.value)
      }

      // return the new state
      return newState
    case 'config/fetchConfigSuccess':
      return {...state, ...action.config}
    case 'elements/fetchConfigInit':
    case 'elements/fetchElementsInit':
    case 'elements/fetchElementInit':
    case 'elements/storeElementInit':
    case 'elements/createElementInit':
    case 'elements/deleteElementInit':
    case 'import/uploadFileInit':
    case 'import/importElementsInit':
      return {...state, pending: true }
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
    case 'import/uploadFileSuccess':
    case 'import/uploadFileError':
    case 'import/importElementsSuccess':
    case 'import/importElementsError':
      return {...state, pending: false }
    default:
      return state
  }
}
