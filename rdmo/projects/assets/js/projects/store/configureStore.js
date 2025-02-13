import { createStore, applyMiddleware, combineReducers } from 'redux'
import thunk from 'redux-thunk'

import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'

import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'

import projectsReducer from '../reducers/projectsReducer'
import userReducer from '../reducers/userReducer'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'

import * as userActions from '../actions/userActions'
import * as projectsActions from '../actions/projectsActions'

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

  const initialState = {
    config: {
      prefix: 'rdmo.projects'
    }
  }

  const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(...middlewares)
  )

  window.addEventListener('load', () => {
    getConfigFromLocalStorage(initialState.config.prefix).forEach(([path, value]) => {
      store.dispatch(configActions.updateConfig(path, value, false))
    })

    Promise.all([
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectsActions.fetchCatalogs())
    ]).then(() => {
      const currentUser = store.getState().currentUser.currentUser
      const isManager = userIsManager(currentUser)
      if (isManager && store.getState().config.myProjects) {
        store.dispatch(configActions.updateConfig('params.user', currentUser.id, false))
      }
      store.dispatch(projectsActions.fetchProjects())
      store.dispatch(projectsActions.fetchInvitations(currentUser.id))
      store.dispatch(projectsActions.fetchAllowedFileTypes())
      store.dispatch(projectsActions.fetchImportUrls())
    })
  })

  return store
}
