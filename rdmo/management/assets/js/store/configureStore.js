import { applyMiddleware, combineReducers, createStore } from 'redux'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import configReducer from 'rdmo/core/assets/js/reducers/configReducer'
import pendingReducer from 'rdmo/core/assets/js/reducers/pendingReducer'
import { getConfigFromLocalStorage } from 'rdmo/core/assets/js/utils/config'
import { siteId } from 'rdmo/core/assets/js/utils/meta'
import { checkStoreId, configureMiddleware } from 'rdmo/core/assets/js/utils/store'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

import * as elementActions from '../actions/elementActions'
import elementsReducer from '../reducers/elementsReducer'
import importsReducer from '../reducers/importsReducer'
import { parseLocation } from '../utils/location'

import ConditionsApi from '../api/ConditionsApi'
import ManagementApi from '../api/ManagementApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'
import TasksApi from '../api/TasksApi'

export default function configureStore() {
  // empty localStorage in new session
  checkStoreId()

  const rootReducer = combineReducers({
    config: configReducer,
    elements: elementsReducer,
    imports: importsReducer,
    pending: pendingReducer
  })

  const initialState = {
    config: {
      prefix: 'rdmo.management.config'
    }
  }

  const store = createStore(
    rootReducer,
    initialState,
    applyMiddleware(...configureMiddleware())
  )

  // load: fetch some of the data which does not change
  const fetchConfig = () => {
    return Promise.all([
      ConditionsApi.fetchRelations(),
      CoreApi.fetchGroups(),
      CoreApi.fetchSettings(),
      CoreApi.fetchSites(),
      ManagementApi.fetchMeta(),
      OptionsApi.fetchAdditionalInputs(),
      OptionsApi.fetchProviders(),
      QuestionsApi.fetchValueTypes(),
      QuestionsApi.fetchWidgetTypes(),
      TasksApi.fetchTaskTypes(),
      TasksApi.fetchTaskAreas(),
    ]).then(([
      relations, groups, settings, sites, meta,
      additionalInputs, providers, valueTypes, widgetTypes, taskTypes, taskAreas]) => {
      store.dispatch(configActions.updateConfig('relations', relations, false))
      store.dispatch(configActions.updateConfig('groups', groups, false))
      store.dispatch(configActions.updateConfig('settings', settings, false))
      store.dispatch(configActions.updateConfig('sites', sites, false))
      store.dispatch(configActions.updateConfig('meta', meta, false))
      store.dispatch(configActions.updateConfig('additionalInputs', additionalInputs, false))
      store.dispatch(configActions.updateConfig('providers', providers, false))
      store.dispatch(configActions.updateConfig('valueTypes', valueTypes, false))
      store.dispatch(configActions.updateConfig('widgetTypes', widgetTypes, false))
      store.dispatch(configActions.updateConfig('taskTypes', taskTypes, false))
      store.dispatch(configActions.updateConfig('taskAreas', taskAreas, false))
    }
    )
  }

  // load, popstate: fetch elements depending on the location
  const fetchElementsFromLocation = () => {
    const { elementType, elementId, elementAction } = parseLocation()
    if (isNil(elementId)) {
      if (isNil(elementAction)) {
        return store.dispatch(elementActions.fetchElements(elementType))
      } else {
        return store.dispatch(elementActions.createElement(elementType))
      }
    } else {
      return store.dispatch(elementActions.fetchElement(elementType, elementId, elementAction))
    }
  }

  // this event is triggered when the page first loads
  window.addEventListener('load', () => {
    getConfigFromLocalStorage(initialState.config.prefix).forEach(([path, value]) => {
      store.dispatch(configActions.updateConfig(path, value, false))
    })

    fetchConfig().then(() => fetchElementsFromLocation()).then(() => {
      if (!isEmpty(siteId) && isEmpty(store.getState().config.filter) && store.getState().config.settings.multisite) {
        store.dispatch(configActions.updateConfig('filter.sites', siteId))
      }
    })
  })

  // this event is triggered when when the forward/back buttons are used
  window.addEventListener('popstate', () => {
    fetchElementsFromLocation()
  })

  return store
}
