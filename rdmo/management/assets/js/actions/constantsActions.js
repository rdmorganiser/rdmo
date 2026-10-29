import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { actions as errorActions } from 'rdmo/core/assets/js/reducers/errorsSlice'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

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
        dispatch(errorActions.setError({
          source: 'relations',
          error: { ...serializeError(error), context: gettext('Relations') }
        }))
        throw error
      }),
      ManagementApi.fetchMeta().catch(error => {
        dispatch(errorActions.setError({
          source: 'meta',
          error: { ...serializeError(error), context: gettext('Metadata') }
        }))
        throw error
      }),
      OptionsApi.fetchAdditionalInputs().catch(error => {
        dispatch(errorActions.setError({
          source: 'additionalInputs',
          error: { ...serializeError(error), context: gettext('Additional inputs') }
        }))
        throw error
      }),
      OptionsApi.fetchProviders().catch(error => {
        dispatch(errorActions.setError({
          source: 'providers',
          error: { ...serializeError(error), context: gettext('Option providers') }
        }))
        throw error
      }),
      QuestionsApi.fetchValueTypes().catch(error => {
        dispatch(errorActions.setError({
          source: 'valueTypes',
          error: { ...serializeError(error), context: gettext('Value types') }
        }))
        throw error
      }),
      QuestionsApi.fetchWidgetTypes().catch(error => {
        dispatch(errorActions.setError({
          source: 'widgetTypes',
          error: { ...serializeError(error), context: gettext('Widget types') }
        }))
        throw error
      }),
      TasksApi.fetchTaskTypes().catch(error => {
        dispatch(errorActions.setError({
          source: 'taskTypes',
          error: { ...serializeError(error), context: gettext('Task types') }
        }))
        throw error
      }),
      TasksApi.fetchTaskAreas().catch(error => {
        dispatch(errorActions.setError({
          source: 'taskAreas',
          error: { ...serializeError(error), context: gettext('Task areas') }
        }))
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
