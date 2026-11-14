import { configureStore as configureToolkitStore } from '@reduxjs/toolkit'
import { isNil } from 'lodash'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as settingsActions from 'rdmo/core/assets/js/actions/settingsActions'
import * as templateActions from 'rdmo/core/assets/js/actions/templateActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'
import configReducer from 'rdmo/core/assets/js/reducers/configSlice'
import errorsReducer from 'rdmo/core/assets/js/reducers/errorsSlice'
import groupsReducer from 'rdmo/core/assets/js/reducers/groupsSlice'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingSlice'
import settingsReducer from 'rdmo/core/assets/js/reducers/settingsSlice'
import sitesReducer from 'rdmo/core/assets/js/reducers/sitesSlice'
import staleReducer from 'rdmo/core/assets/js/reducers/staleSlice'
import templateReducer from 'rdmo/core/assets/js/reducers/templateSlice'
import userReducer from 'rdmo/core/assets/js/reducers/userSlice'
import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'
import { checkStoreId, configureStaleRefresh } from 'rdmo/core/assets/js/utils/store'

import rolesReducer from '../../common/reducers/rolesSlice'
import { selectPermissions } from '../../common/selectors/permissions'
import * as integrationActions from '../actions/integrationActions'
import * as issueActions from '../actions/issueActions'
import * as navigationActions from '../actions/navigationActions'
import * as projectActions from '../actions/projectActions'
import contactReducer from '../reducers/contactSlice'
import documentReducer from '../reducers/documentSlice'
import integrationReducer from '../reducers/integrationSlice'
import interviewReducer from '../reducers/interviewSlice'
import issueReducer from '../reducers/issueSlice'
import locationReducer from '../reducers/locationSlice'
import membershipReducer from '../reducers/membershipSlice'
import projectReducer from '../reducers/projectSlice'
import snapshotReducer from '../reducers/snapshotSlice'
import { parseLocation } from '../utils/location'
import { projectId } from '../utils/meta'

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
      location: locationReducer,
      errors: errorsReducer,
      pending: pendingReducer,
      project: projectReducer,
      membership: membershipReducer,
      snapshot: snapshotReducer,
      document: documentReducer,
      issue: issueReducer,
      integration: integrationReducer,
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
    projectIssues: () => store.dispatch(issueActions.fetchProjectIssues())
  })

  const initDashboardFromLocation = () => {
    const location = parseLocation()
    store.dispatch(navigationActions.navigateDashboard(location))
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    getConfigFromLocalStorage('rdmo.project')
      .forEach(([path, value]) => {
        store.dispatch(configActions.updateConfig(path, value))
      })

    Promise.all([
      store.dispatch(settingsActions.fetchSettings()),
      store.dispatch(templateActions.fetchTemplates()),
      store.dispatch(userActions.fetchCurrentUser()),
      store.dispatch(projectActions.fetchProject())
    ]).then(() => {
      const state = store.getState()
      const project = state.project.project
      const permissions = selectPermissions(state)

      // visibility is rendered in sidebar
      if (permissions.can_view_visibility) {
        if (!isNil(project.visibility)) {
          store.dispatch(projectActions.fetchProjectVisibility(projectId))
        }
      }
      // conditional rendering of Integrations link in sidebar depends on available providers
      if (permissions.can_add_integration || permissions.can_change_integration) {
        store.dispatch(integrationActions.fetchProviders())
      }
      // integrations are used in the Integrations area and the Send task modal
      if (permissions.can_view_integration) {
        store.dispatch(integrationActions.fetchProjectIntegrations(projectId))
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
