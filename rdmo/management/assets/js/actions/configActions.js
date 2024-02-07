import get from 'lodash/get'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'
import ManagementApi from '../api/ManagementApi'
import ConditionsApi from '../api/ConditionsApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'

import { elementTypes } from '../constants/elements'
import { findDescendants } from '../utils/elements'


export function fetchConfig() {
  return (dispatch) => Promise.all([
    ConditionsApi.fetchRelations(),
    CoreApi.fetchGroups(),
    CoreApi.fetchSettings(),
    CoreApi.fetchSites(),
    ManagementApi.fetchMeta(),
    OptionsApi.fetchAdditionalInputs(),
    OptionsApi.fetchProviders(),
    QuestionsApi.fetchValueTypes(),
    QuestionsApi.fetchWidgetTypes()
  ]).then(([relations, groups, settings, sites, meta, additionalInputs, providers,
            valueTypes, widgetTypes]) => dispatch(fetchConfigSuccess({
    relations, groups, settings, sites, meta, additionalInputs, providers, valueTypes, widgetTypes
  })))
}

export function fetchConfigSuccess(config) {
  return {type: 'config/fetchConfigSuccess', config}
}

export function fetchConfigError(errors) {
  return {type: 'elements/fetchConfigError', errors}
}

export function updateConfig(path, value) {
  return {type: 'config/updateConfig', path, value}
}

export function toggleElements(element) {
  return (dispatch, getState) => {
    const path = `display.elements.${elementTypes[element.model]}.${element.id}`
    const value = !get(getState().config, path, true)
    dispatch(updateConfig(path, value))
  }
}

export function toggleDescandants(element, elementType) {
  return (dispatch) => {
    findDescendants(element, elementType).forEach(e => dispatch(toggleElements(e)))
  }
}
