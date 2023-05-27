import { applyMiddleware, createStore } from 'redux'
import thunk from 'redux-thunk'
import ls from 'local-storage'
import isNil from 'lodash/isNil'

import { parseLocation } from '../utils/location'
import { lsKeys } from '../constants/config'

import rootReducer from '../reducers/rootReducer'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

export default function configureStore() {
  const middlewares = [thunk]

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
  )

  // load: fetch some of the data which does not change
  const fetchConfig = () => store.dispatch(configActions.fetchConfig())

  // load: restore the config from the local storage
  const updateConfigFromLocalStorage = () => {
    Object.entries(lsKeys).forEach(([path, defaultValue]) => {
      let value = ls.get(`rdmo.management.config.${path}`)
      if (isNil(value)) {
        switch(defaultValue) {
          case 'true':
            value = false
            break
          case 'false':
            value = false
            break
          default:
            value = defaultValue
        }
      }
      store.dispatch(configActions.updateConfig(path, value))
    })
  }

  // load, popstate: fetch elements depending on the location
  const fetchElementsFromLocation = () => {
    const baseUrl = store.getState().config.baseUrl
    const pathname = window.location.pathname
    let { elementType, elementId, elementAction } = parseLocation(baseUrl, pathname)

    if (isNil(elementType)) {
      elementType = 'catalogs'
    }
    if (isNil(elementId)) {
      if (isNil(elementAction)) {
        return store.dispatch(elementActions.fetchElements(elementType))
      } else {
        return store.dispatch(elementActions.createElement(elementType))
      }
    } else {
      return store.dispatch(elementActions.fetchElement(elementType, elementId, elementAction))
    }
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    updateConfigFromLocalStorage()
    fetchConfig().then(() => fetchElementsFromLocation())
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchElementsFromLocation()
  })

  return store
}
