import CoreApi from 'rdmo/core/assets/js/api/CoreApi'
import ManagementApi from '../api/ManagementApi'
import ConditionsApi from '../api/ConditionsApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'

export function updateConfig(path, value) {
  return {type: 'config/updateConfig', path, value}
}

export function fetchConfig() {
  return (dispatch) => Promise.all([
    ConditionsApi.fetchRelations(),
    CoreApi.fetchGroups(),
    CoreApi.fetchSettings(),
    CoreApi.fetchSites(),
    ManagementApi.fetchMeta(),
    OptionsApi.fetchProviders(),
    QuestionsApi.fetchValueTypes(),
    QuestionsApi.fetchWidgetTypes()
  ]).then(([relations, groups, settings, sites, meta, providers,
            valueTypes, widgetTypes]) => dispatch(fetchConfigSuccess({
    relations, groups, settings, sites, meta, providers, valueTypes, widgetTypes
  })))
}

export function fetchConfigSuccess(config) {
  return {type: 'config/fetchConfigSuccess', config}
}

export function fetchConfigError(errors) {
  return {type: 'elements/fetchConfigError', errors}
}
