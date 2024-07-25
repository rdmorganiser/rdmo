import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import Cookies from 'js-cookie'
import isEmpty from 'lodash/isEmpty'
import rootReducer from '../reducers/rootReducer'
import * as userActions from '../actions/userActions'
import * as projectsActions from '../actions/projectsActions'
import * as configActions from '../actions/configActions'
import userIsManager from '../utils/userIsManager'

export default function configureStore() {
  const middlewares = [thunk]

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

  // load: restore the config from the local storage
  const updateConfigFromLocalStorage = () => {
    const ls = {...localStorage}

    Object.entries(ls).forEach(([lsPath, lsValue]) => {
      if (lsPath.startsWith('rdmo.projects.config.')) {
        const path = lsPath.replace('rdmo.projects.config.', '')
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

    store.dispatch(configActions.updateConfig('params.page', '1'))
  }

  window.addEventListener('load', () => {
    updateConfigFromLocalStorage()
    store.dispatch(userActions.fetchCurrentUser())
    .then(() => {
      const currentUser = store.getState().currentUser.currentUser
      const isManager = userIsManager(currentUser)
      if (isManager && store.getState().config.myProjects) {
        store.dispatch(configActions.updateConfig('params.user', currentUser.id))
      }
      store.dispatch(projectsActions.fetchAllProjects())
      store.dispatch(projectsActions.fetchInvitations(currentUser.id))
      store.dispatch(projectsActions.fetchCatalogs())
      store.dispatch(projectsActions.fetchAllowedFileTypes())
      store.dispatch(projectsActions.fetchImportUrls())
      store.dispatch(projectsActions.fetchSettings())
    })
  })

  return store
}
