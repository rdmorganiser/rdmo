import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'
import ls from 'local-storage'

import { parseLocation } from '../utils/location'

import rootReducer from '../reducers/rootReducer'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

export default function configureStore() {
  const store = createStore(
    rootReducer,
    applyMiddleware(thunk)
  )

  // add a listener to restore the config from the local storage
  const updateConfigFromLocalStorage = (event) => {
    const config = ls.get('rdmo.management.config')
    store.dispatch(configActions.updateConfig(config))
  }
  window.addEventListener('load', updateConfigFromLocalStorage)

  // add listeners for load and popstate
  const fetchElementsFromLocation = (event) => {
    const baseUrl = store.getState().config.baseUrl
    const pathname = event.target.location.pathname
    const { elementType, elementId } = parseLocation(baseUrl, pathname)

    store.dispatch(elementActions.fetchElements(elementType))
  }
  window.addEventListener('load', fetchElementsFromLocation)
  window.addEventListener('popstate', fetchElementsFromLocation)

  return store
}
