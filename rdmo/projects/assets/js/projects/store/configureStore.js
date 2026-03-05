import { createStore, applyMiddleware, combineReducers } from 'redux'

import { checkStoreId, configureMiddleware } from 'rdmo/core/assets/js/utils/store'

import { getConfigFromLocalStorage, isTruthy } from 'rdmo/core/assets/js/utils/config'

import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'
import projectsReducer from '../reducers/projectsReducer'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsReducer'
import userReducer from 'rdmo/core/assets/js/reducers/userReducer'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'

import * as projectsActions from '../actions/projectsActions'

export default function configureStore() {
  // empty localStorage in new session
  checkStoreId()

  const rootReducer = combineReducers({
    config: configReducer,
    currentUser: userReducer,
    pending: pendingReducer,
    projects: projectsReducer,
    settings: settingsReducer,
  })

  const initialState = {
    config: {
      myProjects: true,
      prefix: 'rdmo.projects.config'
    }
  }

  const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(...configureMiddleware())
  )

  window.addEventListener('load', () => {
    getConfigFromLocalStorage(initialState.config.prefix)
      .map(([path, value]) => (
        [path, (path == 'myProjects') ? isTruthy(value) : value]  // cast myProjects to bool
      ))
      .forEach(([path, value]) => {
        store.dispatch(configActions.updateConfig(path, value, false))
      })

    Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectsActions.fetchCatalogs())
    ]).then(() => {
      store.dispatch(projectsActions.fetchProjects())
      store.dispatch(projectsActions.fetchInvitations())
      store.dispatch(projectsActions.fetchAllowedFileTypes())
      store.dispatch(projectsActions.fetchImportUrls())
    })
  })

  return store
}
