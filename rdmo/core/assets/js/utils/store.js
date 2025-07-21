import thunk from 'redux-thunk'
import Cookies from 'js-cookie'
import isEmpty from 'lodash/isEmpty'

export const configureMiddleware = () => {
  const middlewares = [thunk]

  if (process.env.NODE_ENV === 'development') {
    const { logger } = require('redux-logger')
    middlewares.push(logger)
  }

  return middlewares
}

export const checkStoreId = () => {
  const currentStoreId = Cookies.get('storeid')
  const localStoreId = localStorage.getItem('rdmo.storeid')

  if (isEmpty(localStoreId) || localStoreId !== currentStoreId) {
    localStorage.clear()
    localStorage.setItem('rdmo.storeid', currentStoreId)
  }
}
