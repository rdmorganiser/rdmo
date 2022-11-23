const initialState = {
  baseUrl: '/management/'
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case 'config/updateConfig':
      return Object.assign({}, state, action.config)
    default:
      return state
  }
}
