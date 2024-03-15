import { applyMiddleware, createStore } from 'redux'
import Cookies from 'js-cookie'
import thunk from 'redux-thunk'
import isEmpty from 'lodash/isEmpty'

import rootReducer from '../reducers/rootReducer'

import * as configActions from '../actions/configActions'
import * as pageActions from '../actions/pageActions'

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

  const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
  )

  const fetchConfig = () => store.dispatch(configActions.fetchConfig())

  const fetchPage = () => store.dispatch(pageActions.fetchPage())

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    fetchConfig().then(() => fetchPage())
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {

  })

  return store
}
