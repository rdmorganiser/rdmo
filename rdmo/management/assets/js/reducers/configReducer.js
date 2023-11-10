import set from 'lodash/set'

import rdmoBaseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const initialState = {
  baseUrl: rdmoBaseUrl + '/management/',
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
