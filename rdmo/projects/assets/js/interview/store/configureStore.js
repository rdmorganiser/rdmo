import { applyMiddleware, createStore, combineReducers } from 'redux'
import Cookies from 'js-cookie'
import thunk from 'redux-thunk'
import isEmpty from 'lodash/isEmpty'

import configReducer from '../reducers/configReducer'
import interviewReducer from '../reducers/interviewReducer'

import * as configActions from '../actions/configActions'
import * as interviewActions from '../actions/interviewActions'

import { parseLocation } from '../utils/location'

export default function configureStore() {
  const middlewares = [thunk]

  // empty localStorage in new session
  const currentStoreId = Cookies.get('storeid')
  const localStoreId = localStorage.getItem('rdmo.storeid')

  if (isEmpty(localStoreId) || localStoreId !== currentStoreId) {
    localStorage.clear()
    localStorage.setItem('rdmo.storeid', currentStoreId)
  }

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  const rootReducer = combineReducers({
    config: configReducer,
    interview: interviewReducer
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
    Promise.all([
      store.dispatch(configActions.fetchConfig()),
      store.dispatch(interviewActions.fetchOverview()),
      store.dispatch(interviewActions.fetchProgress())
    ]).then(() => fetchPageFromLocation())
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchPageFromLocation()
  })

  return store
}
