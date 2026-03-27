import { applyMiddleware, combineReducers, createStore } from 'redux'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'
import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsReducer'
import templateReducer from 'rdmo/core/assets/js/reducers/templateReducer'
import userReducer from 'rdmo/core/assets/js/reducers/userReducer'
import { getConfigFromLocalStorage, isTruthy } from 'rdmo/core/assets/js/utils/config'
import { checkStoreId, configureMiddleware } from 'rdmo/core/assets/js/utils/store'

import * as rolesActions from '../../common/actions/rolesActions'
import rolesReducer from '../../common/reducers/rolesReducer'
import * as projectsActions from '../actions/projectsActions'
import projectsReducer from '../reducers/projectsReducer'

export default function configureStore() {
  // empty localStorage in new session
  checkStoreId()

  const rootReducer = combineReducers({
    config: configReducer,
    currentUser: userReducer,
    pending: pendingReducer,
    projects: projectsReducer,
    settings: settingsReducer,
    templates: templateReducer,
    roles: rolesReducer
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
