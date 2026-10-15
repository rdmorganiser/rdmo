import { get, isNil, pick } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { locationKeys, updateLocation } from '../utils/location'

import { fetchPage } from './interviewActions'
import { clearCurrentView, fetchAnswers, fetchView  } from './projectActions'

export function navigateDashboard(location, back = null) {
  return (dispatch, getState) => {
    const updateLocationAndConfig = (location) => {
      // update the location in the url
      updateLocation(location)

      // update the location in the config store
      locationKeys.forEach(key => dispatch(updateConfig(key, location[key] ?? null, false)))
    }

    // the config still holds the location we are navigating away from
    const currentLocation = pick(getState().config, locationKeys)

    // store unsaved defaults when leaving an interview page
    const storeDefaults = () => (
      (currentLocation.area == 'interview' && !isNil(currentLocation.pageId)) ? (
        dispatch(storeDefaultValues())
      ) : (
        Promise.resolve()
      )
    )

    return storeDefaults().then(() => {
      // for the interview, the location and config are updated after the page is fetched, since pages might be skipped
      if (location.area == 'interview') {
        // /interview/
        if (isNil(location.pageId)) {
          dispatch(fetchContinue())
          dispatch(fetchNavigation())
          dispatch(fetchProgress())
          updateLocationAndConfig(location)
        } else {
          return dispatch(fetchPage(location.pageId, back)).then((page) => {
            if (page) {
              updateLocationAndConfig({...location, pageId: page.id})
            } else if (getState().interview.done) {
              dispatch(navigateDashboard({area: 'interview'}))
            } else {
              updateLocationAndConfig(location)
            }
          })
        }
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
        hide_answers: location.detail == 'questions' ? 'true' : 'false'
      }))
    } else {
      dispatch(clearCurrentView())
    }
  }
}
