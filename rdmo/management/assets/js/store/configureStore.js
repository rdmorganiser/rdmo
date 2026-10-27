import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as groupsActions from 'rdmo/core/assets/js/actions/groupsActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as sitesActions from 'rdmo/core/assets/js/actions/sitesActions'
import configReducer from 'rdmo/core/assets/js/reducers/configSlice'
import groupsReducer from 'rdmo/core/assets/js/reducers/groupsSlice'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingSlice'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsSlice'
import sitesReducer from 'rdmo/core/assets/js/reducers/sitesSlice'
import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'
import { siteId } from 'rdmo/core/assets/js/utils/meta'
import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import * as constantsActions from '../actions/constantsActions'
import * as elementActions from '../actions/elementActions'
import constantsReducer from '../reducers/constantsSlice'
import elementsReducer from '../reducers/elementsSlice'
import importsReducer from '../reducers/importsSlice'
import { parseLocation } from '../utils/location'

import { configureStore as configureToolkitStore } from '@reduxjs/toolkit'

export default function configureStore() {
  // empty localStorage in new session
  checkStoreId()

  const middlewares = []

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  const initialState = {
    config: {
      prefix: 'rdmo.management.config'
    }
  }

  const store = configureToolkitStore({
    reducer: {
      config: configReducer,
      elements: elementsReducer,
      imports: importsReducer,
      pending: pendingReducer,
      constants: constantsReducer,
      settings: settingsReducer,
      sites: sitesReducer,
      groups: groupsReducer
    },
    preloadedState: initialState,
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(middlewares)
  })

  // load: fetch some of the data which does not change
  const fetchConstants = () => {
    return Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(sitesActions.fetchSites()),
      store.dispatch(groupsActions.fetchGroups()),
      store.dispatch(constantsActions.fetchConstants()),
    ])
  }

  // load, popstate: fetch elements depending on the location
  const fetchElementsFromLocation = () => {
    const { elementType, elementId, elementAction } = parseLocation()
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
    getConfigFromLocalStorage(initialState.config.prefix).forEach(([path, value]) => {
      store.dispatch(configActions.updateConfig(path, value, false))
    })

    fetchConstants().then(() => fetchElementsFromLocation()).then(() => {
      if (!isEmpty(siteId) && isEmpty(store.getState().config.filter) && store.getState().settings.multisite) {
        store.dispatch(configActions.updateConfig('filter.sites', siteId))
      }
    })
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchElementsFromLocation()
  })

  return store
}
