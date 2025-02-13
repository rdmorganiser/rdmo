import { createStore, applyMiddleware, combineReducers } from 'redux'
import thunk from 'redux-thunk'

import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'

import configReducer from '../reducers/configReducer'
import projectsReducer from '../reducers/projectsReducer'
import userReducer from '../reducers/userReducer'

import * as userActions from '../actions/userActions'
import * as projectsActions from '../actions/projectsActions'
import * as configActions from '../actions/configActions'

import userIsManager from '../utils/userIsManager'

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
    currentUser: userReducer,
    projects: projectsReducer,
    pending: pendingReducer
  })

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
  }

  window.addEventListener('load', () => {
    updateConfigFromLocalStorage()

    Promise.all([
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectsActions.fetchCatalogs())
    ]).then(() => {
      const currentUser = store.getState().currentUser.currentUser
      const isManager = userIsManager(currentUser)
      if (isManager && store.getState().config.myProjects) {
        store.dispatch(configActions.updateConfig('params.user', currentUser.id))
      }
      store.dispatch(projectsActions.fetchProjects())
      store.dispatch(projectsActions.fetchInvitations(currentUser.id))
      store.dispatch(projectsActions.fetchAllowedFileTypes())
      store.dispatch(projectsActions.fetchImportUrls())
    })
  })

  return store
}
