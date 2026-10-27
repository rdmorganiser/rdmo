import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'
import configReducer from 'rdmo/core/assets/js/reducers/configSlice'
import errorsReducer from 'rdmo/core/assets/js/reducers/errorsSlice'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingSlice'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsSlice'
import templateReducer from 'rdmo/core/assets/js/reducers/templateSlice'
import userReducer from 'rdmo/core/assets/js/reducers/userSlice'
import { getConfigFromLocalStorage, isTruthy } from 'rdmo/core/assets/js/utils/config'
import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import * as rolesActions from '../../common/actions/rolesActions'
import rolesReducer from '../../common/reducers/rolesSlice'
import * as projectsActions from '../actions/projectsActions'
import projectsReducer from '../reducers/projectsSlice'

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
      myProjects: true,
      prefix: 'rdmo.projects.config',
      params: {
        ordering: '-last_changed'
      }
    }
  }

  const store = configureToolkitStore({
    reducer: {
      config: configReducer,
      errors: errorsReducer,
      currentUser: userReducer,
      pending: pendingReducer,
      projects: projectsReducer,
      settings: settingsReducer,
      templates: templateReducer,
      roles: rolesReducer
    },
    preloadedState: initialState,
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(middlewares)
  })

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
      store.dispatch(templateActions.fetchTemplates()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectsActions.fetchCatalogs()),
      store.dispatch(rolesActions.fetchRoles())
    ]).then(() => {
      store.dispatch(projectsActions.fetchProjects())
      store.dispatch(projectsActions.fetchInvitations())
      store.dispatch(projectsActions.fetchAllowedFileTypes())
      store.dispatch(projectsActions.fetchImportUrls())
    })
  })

  return store
}
