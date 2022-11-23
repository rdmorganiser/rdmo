import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'

import { parseLocation } from 'rdmo/core/assets/js/utils/location'

import rootReducer from '../reducers/rootReducer'

import * as configActions from '../actions/configActions'

export default function configureStore() {
  const store = createStore(
    rootReducer,
    applyMiddleware(thunk)
  )

  // add listeners for load and popstate
  const getConfigFromLocation = (event) => {
    const config = parseLocation(store.getState().config.baseUrl, event.target.location.pathname)
    store.dispatch(configActions.updateConfig(config))
  }
  window.addEventListener('load', getConfigFromLocation)
  window.addEventListener('popstate', getConfigFromLocation)

  return store
}
