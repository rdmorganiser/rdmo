import { applyMiddleware, createStore, combineReducers } from 'redux'
import thunk from 'redux-thunk'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'

import { parseLocation } from '../utils/location'

import configReducer from '../reducers/configReducer'
import elementsReducer from '../reducers/elementsReducer'
import importsReducer from '../reducers/importsReducer'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

export default function configureStore() {
  // empty localStorage in new session
  checkStoreId()

  const middlewares = [thunk]

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  const rootReducer = combineReducers({
    config: configReducer,
    elements: elementsReducer,
    imports: importsReducer,
    pending: pendingReducer
  })

  const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
  )

  // load: fetch some of the data which does not change
  const fetchConfig = () => store.dispatch(configActions.fetchConfig())

  // load: restore the config from the local storage
  const updateConfigFromLocalStorage = () => {
    const ls = {...localStorage}
    Object.entries(ls).forEach(([lsPath, lsValue]) => {
      if (lsPath.startsWith('rdmo.management.config.')) {
        const path = lsPath.replace('rdmo.management.config.', '')
        let value
        switch(lsValue) {
          case 'true':
            value = true
            break
          case 'false':
            value = false
            break
          default:
            value = lsValue
        }
        store.dispatch(configActions.updateConfig(path, value))
      }
    })
  }

  let currentSiteId
  // load, popstate: fetch elements depending on the location
  const fetchElementsFromLocation = () => {
    const baseUrl = store.getState().config.baseUrl
    currentSiteId = store.getState().config.currentSite?.id.toString() || ''
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
    fetchConfig().then(() => {
      fetchElementsFromLocation()
      if (!isEmpty(currentSiteId) && isEmpty(store.getState().config.filter) && store.getState().config.settings.multisite) {
        store.dispatch(configActions.updateConfig('filter.sites', currentSiteId))
      }
    })

  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchElementsFromLocation()
  })

  return store
}
