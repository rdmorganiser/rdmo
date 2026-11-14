import * as errorActions from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

import { actions } from '../reducers/constantsSlice'

import ConditionsApi from '../api/ConditionsApi'
import ManagementApi from '../api/ManagementApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'
import TasksApi from '../api/TasksApi'

export function fetchConstants() {
  const pendingId = 'fetchConstants'

  return function(dispatch) {
    dispatch(addToPending(pendingId))

    return Promise.all([
      ConditionsApi.fetchRelations().catch(error => {
        dispatch(errorActions.setError('relations', error, gettext('Relations')))
        throw error
      }),
      ManagementApi.fetchMeta().catch(error => {
        dispatch(errorActions.setError('meta', error, gettext('Metadata')))
        throw error
      }),
      OptionsApi.fetchAdditionalInputs().catch(error => {
        dispatch(errorActions.setError('additionalInputs', error, gettext('Additional inputs')))
        throw error
      }),
      OptionsApi.fetchProviders().catch(error => {
        dispatch(errorActions.setError('providers', error, gettext('Option providers')))
        throw error
      }),
      QuestionsApi.fetchValueTypes().catch(error => {
        dispatch(errorActions.setError('valueTypes', error, gettext('Value types')))
        throw error
      }),
      QuestionsApi.fetchWidgetTypes().catch(error => {
        dispatch(errorActions.setError('widgetTypes', error, gettext('Widget types')))
        throw error
      }),
      TasksApi.fetchTaskTypes().catch(error => {
        dispatch(errorActions.setError('taskTypes', error, gettext('Task types')))
        throw error
      }),
      TasksApi.fetchTaskAreas().catch(error => {
        dispatch(errorActions.setError('taskAreas', error, gettext('Task areas')))
        throw error
      }),
    ])
      .then(([relations, meta, additionalInputs, providers, valueTypes, widgetTypes, taskTypes, taskAreas]) => (
        dispatch(actions.fetchConstantsSuccess({
          relations,
          meta,
          additionalInputs,
          providers,
          valueTypes,
          widgetTypes,
          taskTypes,
          taskAreas
        }))
      ))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}
