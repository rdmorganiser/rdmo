import { applyMiddleware, combineReducers, createStore } from 'redux'
import thunk from 'redux-thunk'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'
import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsReducer'
import templateReducer from 'rdmo/core/assets/js/reducers/templateReducer'
import userReducer from 'rdmo/core/assets/js/reducers/userReducer'
import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'
import { checkStoreId } from 'rdmo/core/assets/js/utils/store'

import * as rolesActions from '../../common/actions/rolesActions'
import rolesReducer from '../../common/reducers/rolesReducer'
import * as projectActions from '../actions/projectActions'
import projectReducer from '../reducers/projectReducer'
import { parseLocation } from '../utils/location'
import { projectId } from '../utils/meta'

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
    pending: pendingReducer,
    project: projectReducer,
    settings: settingsReducer,
    templates: templateReducer,
    user: userReducer,
    roles: rolesReducer
  })

  const initialState = {
    config: {
      prefix: 'rdmo.project'
    }
  }

  const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(...middlewares)
  )

  const initDashboardFromLocation = () => {
    const location = parseLocation()
    store.dispatch(projectActions.navigateDashboard(location))
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    getConfigFromLocalStorage('rdmo.project').forEach(([path, value]) => {
      store.dispatch(configActions.updateConfig(path, value))
    })

    Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(templateActions.fetchTemplates()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectActions.fetchProject()),
      store.dispatch(rolesActions.fetchRoles())
    ]).then(() => {
      const permissions = store.getState().project.project.project.permissions
      if (permissions.can_view_invite) {
        store.dispatch(projectActions.fetchProjectInvites(projectId))
      }
      initDashboardFromLocation()
    })
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    initDashboardFromLocation()
  })

  return store
}
