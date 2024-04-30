import { applyMiddleware, createStore, combineReducers } from 'redux'
import thunk from 'redux-thunk'

// import { checkStoreId } from 'rdmo/core/assets/js/utils/store'
import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'

import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsReducer'
import templateReducer from 'rdmo/core/assets/js/reducers/templateReducer'
import userReducer from 'rdmo/core/assets/js/reducers/userReducer'

import interviewReducer from '../reducers/interviewReducer'
import projectReducer from '../reducers/projectReducer'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'

import * as interviewActions from '../actions/interviewActions'
import * as projectActions from '../actions/projectActions'

import { parseLocation } from '../utils/location'

export default function configureStore() {
  // empty localStorage in new session
  // checkStoreId()

  const middlewares = [thunk]

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  const rootReducer = combineReducers({
    config: configReducer,
    interview: interviewReducer,
    project: projectReducer,
    settings: settingsReducer,
    templates: templateReducer,
    user: userReducer,
  })

  const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
  )

  const fetchPageFromLocation = () => {
    const { pageId } = parseLocation()
    store.dispatch(interviewActions.fetchPage(pageId))
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    getConfigFromLocalStorage('rdmo.interview').forEach(([path, value]) => {
      store.dispatch(configActions.updateConfig('rdmo.interview', path, value))
    })

    Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(templateActions.fetchTemplates()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectActions.fetchOverview()),
      store.dispatch(projectActions.fetchProgress())
    ]).then(() => fetchPageFromLocation())
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchPageFromLocation()
  })

  return store
}
