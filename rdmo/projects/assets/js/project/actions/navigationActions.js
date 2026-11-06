import { get, isNil } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { fetchContinue, fetchPage, storeDefaultValues } from './interviewActions'
import { setLocation } from './locationActions'
import { clearCurrentView, fetchAnswers, fetchNavigation, fetchProgress, fetchView } from './projectActions'

export function navigateDashboard(location, back = null) {
  return (dispatch, getState) => {
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
          dispatch(setLocation(location))
          return
        } else {
          return dispatch(fetchPage(location.pageId, back)).then((page) => {
            if (page) {
              dispatch(setLocation({...location, pageId: page.id}))
            } else if (getState().interview.done) {
              dispatch(navigateDashboard({area: 'interview'}))
            } else {
              dispatch(setLocation(location))
            }
          })
        }
      }

      // for all other areas, the location and store are updated first
      dispatch(setLocation(location))

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
