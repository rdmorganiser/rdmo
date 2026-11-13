import { isNil } from 'lodash'

import * as groupsActions from 'rdmo/core/assets/js/actions/groupsActions'
import * as sitesActions from 'rdmo/core/assets/js/actions/sitesActions'
import { selectConfig } from 'rdmo/core/assets/js/reducers/configSlice'

import * as rolesActions from '../../common/actions/rolesActions'
import { selectPermissions } from '../../common/selectors/permissions'

import { clearCurrentView, fetchAnswers, fetchProjectViews, fetchView } from './documentActions'
import { fetchContinue, fetchPage, storeDefaultValues } from './interviewActions'
import { fetchNavigation, fetchProgress } from './interviewNavigationActions'
import { fetchProjectIssues } from './issueActions'
import { setLocation } from './locationActions'
import { fetchProjectInvites, fetchProjectMemberships } from './membershipActions'
import { fetchCatalogs, fetchProjectHierarchy } from './projectActions'
import { fetchProjectSnapshots } from './snapshotActions'

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

      const state = getState()
      const permissions = selectPermissions(state)

      switch (location.area) {
        case 'dashboard':
          dispatch(fetchProjectIssues())
          break
        case 'information':
          dispatch(fetchProjectHierarchy())
          dispatch(fetchCatalogs())
          if (permissions.can_view_visibility) {
            if (state.settings.multisite && permissions.can_view_site) {
              dispatch(sitesActions.fetchSites())
            }
            if (state.settings.groups && permissions.can_view_group) {
              dispatch(groupsActions.fetchGroups())
            }
          }
          break
        case 'memberships':
          dispatch(rolesActions.fetchRoles())
          dispatch(fetchProjectMemberships())
          if (permissions.can_view_invite) {
            dispatch(fetchProjectInvites())
          }
          break
        case 'documents':
          dispatch(fetchProjectSnapshots())
          dispatch(fetchProjectViews())
          break
        case 'snapshots':
          dispatch(fetchProjectSnapshots())
          if (!isNil(location.snapshotId)) {
            dispatch(fetchProjectViews())
          }
          break
      }

      if (!isNil(location.viewId)) {
        // /documents/views/
        dispatch(fetchView(location.snapshotId, location.viewId))
      } else if (['questions', 'answers'].includes(location.detail)) {
        // /documents/questions/ and /documents/answers/
        dispatch(fetchAnswers(location.snapshotId, {
          include_help: selectConfig(getState(), 'document.includeHelp', false),
          hide_answers: location.detail == 'questions' ? 'true' : 'false'
        }))
      } else {
        dispatch(clearCurrentView())
      }
    })
  }
}
