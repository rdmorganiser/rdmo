import { isNil } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { locationKeys, updateLocation } from '../utils/location'

import * as actionTypes from './actionTypes'
import { fetchAnswers, fetchNavigation, fetchView} from './projectActions'

export function navigateDashboard(location) {
  return (dispatch) => {
    // update the location in the url
    updateLocation(location)

    // update the location in the config store
    locationKeys.forEach(key => dispatch(updateConfig(key, location[key] ?? null, false)))

    if (!isNil(location.viewId)) {
      dispatch(fetchView(location.snapshotId, location.viewId))
    } else if (location.detail == 'answers') {
      dispatch(fetchAnswers(location.snapshotId))
    } else if (location.area == 'interview') {
      dispatch(fetchNavigation())
    } else {
      dispatch({ type: actionTypes.CLEAR_CURRENT_VIEW })
    }
  }
}
