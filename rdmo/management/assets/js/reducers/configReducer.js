import { updateLocation } from '../utils/locations'

const initialState = {
  baseUrl: '/management/'
}

export default function configReducer(state = initialState, action) {

  switch(action.type) {
    case 'config/updateConfig':
      return Object.assign({}, state, action.config)
    case 'config/updateLocation':
      updateLocation(action.config)
      return state
    default:
      return state
  }

}
