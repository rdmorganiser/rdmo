import { parseLocation, updateLocation } from '../utils/locations'

const basePath = '/management/'
const initialState = parseLocation(basePath, window.location.pathname)

export default function configReducer(state = initialState, action) {

  switch(action.type) {
    case 'config/updateConfig':
      return Object.assign({}, state, action.config)
    case 'config/updateConfigAndLocation':
      updateLocation(basePath, action.config)
      return Object.assign({}, state, action.config)
    default:
      return state
  }

}
