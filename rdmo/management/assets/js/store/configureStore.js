import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'
import logger from 'redux-logger'
import ls from 'local-storage'
import isNil from 'lodash/isNil'

import { parseLocation } from '../utils/location'
import { lsKeys } from '../constants/config'

import rootReducer from '../reducers/rootReducer'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

export default function configureStore() {
  const store = createStore(
    rootReducer,
    applyMiddleware(thunk, logger)
  )

  // fetch some of the django settings
  const fetchSettings = (event) => {
    store.dispatch(configActions.fetchSettings())
  }

  // fetch the model meta information
  const fetchMeta = (event) => {
    store.dispatch(configActions.fetchMeta())
  }

  // add a listener to restore the config from the local storage
  const updateConfigFromLocalStorage = (event) => {
    const config = {}
    Object.entries(lsKeys).forEach(([path, defaultValue]) => {
      const value = ls.get(`rdmo.management.config.${path}`) || defaultValue
      store.dispatch(configActions.updateConfig(path, value))
    })
  }
  window.addEventListener('load', updateConfigFromLocalStorage)

  // add listeners for load and popstate
  const fetchElementsFromLocation = (event) => {
    const baseUrl = store.getState().config.baseUrl
    const pathname = event.target.location.pathname
    let { elementType, elementId, elementAction } = parseLocation(baseUrl, pathname)

    if (isNil(elementType)) {
      elementType = 'catalogs'
    }
    if (isNil(elementId)) {
      if (isNil(elementAction)) {
        store.dispatch(elementActions.fetchElements(elementType))
      } else {
        store.dispatch(elementActions.createElement(elementType))
      }
    } else {
      store.dispatch(elementActions.fetchElement(elementType, elementId, elementAction))
    }
  }

  window.addEventListener('load', fetchSettings)
  window.addEventListener('load', fetchMeta)
  window.addEventListener('load', fetchElementsFromLocation)
  window.addEventListener('popstate', fetchElementsFromLocation)

  return store
}
