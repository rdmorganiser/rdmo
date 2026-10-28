import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

import ConditionsApi from '../api/ConditionsApi'
import ManagementApi from '../api/ManagementApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'
import TasksApi from '../api/TasksApi'

import * as actionTypes from './actionTypes'

export function fetchConstants() {
  const pendingId = 'fetchConstants'

  return function(dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_CONSTANTS_INIT })

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
        dispatch({
          type: actionTypes.FETCH_CONSTANTS_SUCCESS, constants: {
            relations,
            meta,
            additionalInputs,
            providers,
            valueTypes,
            widgetTypes,
            taskTypes,
            taskAreas
          }
        })
      ))
      .catch((error) => dispatch({type: actionTypes.FETCH_CONSTANTS_ERROR, error}))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}
