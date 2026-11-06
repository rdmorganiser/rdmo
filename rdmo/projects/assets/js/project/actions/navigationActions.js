import { get, isNil } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { actions as locationActions } from '../reducers/locationSlice'
import { updateLocation } from '../utils/location'

import { fetchContinue, fetchPage, storeDefaultValues } from './interviewActions'
import { clearCurrentView, fetchAnswers, fetchNavigation, fetchProgress, fetchView } from './projectActions'

export function navigateDashboard(location, back = null) {
  return (dispatch, getState) => {
    const updateLocationAndStore = (location) => {
      // update the location in the url
      updateLocation(location)

      // update the location in the location store
      dispatch(locationActions.setLocation(location))
    }

    // the store still holds the location we are navigating away from
    const currentLocation = getState().location

    // store unsaved defaults when leaving an interview page
    const storeDefaults = () => (
      (currentLocation.area == 'interview' && !isNil(currentLocation.pageId)) ? (
        dispatch(storeDefaultValues())
      ) : (
        Promise.resolve()
      )
    )

    return storeDefaults().then(() => {
      // for the interview, the location and store are updated after the page is fetched, since pages might be skipped
      if (location.area == 'interview') {
        // /interview/
        if (isNil(location.pageId)) {
          dispatch(fetchContinue())
          dispatch(fetchNavigation())
          dispatch(fetchProgress())
          updateLocationAndStore(location)
        } else {
          return dispatch(fetchPage(location.pageId, back)).then((page) => {
            if (page) {
              updateLocationAndStore({...location, pageId: page.id})
            } else if (getState().interview.done) {
              dispatch(navigateDashboard({area: 'interview'}))
            } else {
              updateLocationAndStore(location)
            }
          })
        }
      }

      // for all other areas, the location and store are updated first
      updateLocationAndStore(location)

      if (!isNil(location.viewId)) {
        // /documents/views/
        dispatch(fetchView(location.snapshotId, location.viewId))
      } else if (['questions', 'answers'].includes(location.detail)) {
        // /documents/questions/ and /documents/answers/
        dispatch(fetchAnswers(location.snapshotId, {
          include_help: isTruthy(get(getState().config, 'document.includeHelp')),
          hide_answers: location.detail == 'questions' ? 'true' : 'false'
        }))
      } else {
        dispatch(clearCurrentView())
      }
    })
  }
}
