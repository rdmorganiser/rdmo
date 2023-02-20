import ls from 'local-storage'

const initialState = {
  baseUrl: '/management/',
  filterUri: '',
  filterUriPrefix: ''
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case 'config/updateConfig':
      const newState = Object.assign({}, state, action.config)

      // store the new state in the local storage
      ls.set('rdmo.management.config', newState)

      // return the new state
      return newState
    case 'config/fetchSettingsSuccess':
      return Object.assign({}, state, {
        settings: action.settings
      })
    case 'config/fetchMetaSuccess':
      return Object.assign({}, state, {
        meta: action.meta
      })
    default:
      return state
  }
}
