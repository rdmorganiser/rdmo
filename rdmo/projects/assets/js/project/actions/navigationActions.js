import { get, isNil } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { locationKeys, updateLocation } from '../utils/location'

import * as actionTypes from './actionTypes'
import { fetchPage } from './interviewActions'
import { fetchAnswers, fetchView } from './projectActions'

export function navigateDashboard(location, back = null) {
  return (dispatch, getState) => {
    const updateLocationAndConfig = (location) => {
      // update the location in the url
      updateLocation(location)

      // update the location in the config store
      locationKeys.forEach(key => dispatch(updateConfig(key, location[key] ?? null, false)))
    }

    // for the interview, the location and config are updated after the page is fetched, since pages might be skipped
    if (location.area == 'interview') {
      // /interview/
      return dispatch(fetchPage(location.pageId, back)).then((page) => {
        updateLocationAndConfig({...location, pageId: page?.id ?? location.pageId})
      })
    }

    // for all other areas, the location and config are updated first
    updateLocationAndConfig(location)

    if (!isNil(location.viewId)) {
      // /documents/views/
      dispatch(fetchView(location.snapshotId, location.viewId))
    } else if (['questions', 'answers'].includes(location.detail)) {
      // /documents/questions/ and /documents/answers/
      dispatch(fetchAnswers(location.snapshotId, {
        include_help: isTruthy(get(getState().config, 'document.includeHelp')),
        include_answers: location.detail == 'answers' ? 'true' : 'false'
      }))
    } else {
      dispatch({ type: actionTypes.CLEAR_CURRENT_VIEW })
    }
  }
}
