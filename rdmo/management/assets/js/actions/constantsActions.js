import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
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
    dispatch(actions.fetchConstantsInit())

    return Promise.all([
      ConditionsApi.fetchRelations(),
      ManagementApi.fetchMeta(),
      OptionsApi.fetchAdditionalInputs(),
      OptionsApi.fetchProviders(),
      QuestionsApi.fetchValueTypes(),
      QuestionsApi.fetchWidgetTypes(),
      TasksApi.fetchTaskTypes(),
      TasksApi.fetchTaskAreas(),
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
      .catch((error) => dispatch(actions.fetchConstantsError(serializeError(error))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}
