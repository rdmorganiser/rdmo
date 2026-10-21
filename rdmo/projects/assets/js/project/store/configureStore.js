import { isNil } from 'lodash'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as groupsActions from 'rdmo/core/assets/js/actions/groupsActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as sitesActions from 'rdmo/core/assets/js/actions/sitesActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'
import configReducer from 'rdmo/core/assets/js/reducers/configSlice'
import groupsReducer from 'rdmo/core/assets/js/reducers/groupsSlice'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingSlice'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsSlice'
import sitesReducer from 'rdmo/core/assets/js/reducers/sitesSlice'
import staleReducer from 'rdmo/core/assets/js/reducers/staleSlice'
import templateReducer from 'rdmo/core/assets/js/reducers/templateSlice'
import userReducer from 'rdmo/core/assets/js/reducers/userSlice'
import { getConfigFromLocalStorage, isTruthy } from 'rdmo/core/assets/js/utils/config'
import { checkStoreId, configureStaleRefresh } from 'rdmo/core/assets/js/utils/store'

import * as rolesActions from '../../common/actions/rolesActions'
import rolesReducer from '../../common/reducers/rolesSlice'
import { combinePermissions } from '../../common/utils/permissions'
import * as navigationActions from '../actions/navigationActions'
import * as projectActions from '../actions/projectActions'
import contactReducer from '../reducers/contactReducer'
import interviewReducer from '../reducers/interviewReducer'
import projectSliceReducer from '../reducers/projectSlice'
import { parseLocation } from '../utils/location'
import { projectId } from '../utils/meta'

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
      prefix: 'rdmo.project',
      showClosedTasks: false,
      showClosedRecommendations: false
    }
  }

  const store = configureToolkitStore({
    reducer: {
      config: configReducer,
      pending: pendingReducer,
      project: projectSliceReducer,
      settings: settingsReducer,
      templates: templateReducer,
      user: userReducer,
      roles: rolesReducer,
      sites: sitesReducer,
      groups: groupsReducer,
      stale: staleReducer,
      interview: interviewReducer,
      contact: contactReducer,
    },
    preloadedState: initialState,
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(middlewares)
  })

  configureStaleRefresh(store, {
    projectIssues: () => store.dispatch(projectActions.fetchProjectIssues())
  })

  const initDashboardFromLocation = () => {
    const location = parseLocation()
    store.dispatch(navigationActions.navigateDashboard(location))
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    getConfigFromLocalStorage('rdmo.project')
      .map(([path, value]) => (
        [path, ['showClosedTasks', 'showClosedRecommendations', 'showManagement'].includes(path) ? (
          isTruthy(value)
        ) : value]  // cast to bool
      ))
      .forEach(([path, value]) => {
        store.dispatch(configActions.updateConfig(path, value))
      })

    Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(templateActions.fetchTemplates()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectActions.fetchProject()),
      store.dispatch(rolesActions.fetchRoles())
    ]).then(() => {
      const state = store.getState()
      const project = state.project.project.project
      const currentUser = state.user.currentUser

      const permissions = combinePermissions(
        project.permissions,
        currentUser.permissions
      )

      if (permissions.can_view_invite) {
        store.dispatch(projectActions.fetchProjectInvites(projectId))
      }

      if (permissions.can_view_visibility) {
        if (state.settings.multisite && permissions.can_view_site) {
          store.dispatch(sitesActions.fetchSites())
        }
        if (state.settings.groups && permissions.can_view_group) {
          store.dispatch(groupsActions.fetchGroups())
        }
        if (!isNil(project.visibility)) {
          store.dispatch(projectActions.fetchProjectVisibility(projectId))
        }
      }
      if (permissions.can_add_integration || permissions.can_change_integration) {
        store.dispatch(projectActions.fetchProviders())
      }
      if (permissions.can_view_integration) {
        store.dispatch(projectActions.fetchProjectIntegrations(projectId))
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
