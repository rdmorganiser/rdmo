import { isNil } from 'lodash'

import CatalogsApi from 'rdmo/projects/assets/js/common/api/CatalogsApi'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { projectId } from '../utils/meta'
import { locationKeys, updateLocation } from '../utils/location'

import ProjectApi from '../api/ProjectApi'

import * as actionTypes from './actionTypes'

// asynchronous actions

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
    } else {
      dispatch({ type: actionTypes.CLEAR_CURRENT_VIEW })
    }
  }
}

// project

export function fetchProject() {

  return function (dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch({ type: actionTypes.FETCH_PROJECT_INIT })

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectHierarchy(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectViews(projectId),
      ProjectApi.fetchProjectAnswers(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      ProjectApi.fetchProjectMembershipHierarchy(projectId),
      CatalogsApi.fetchCatalogs()
    ])
      .then(([project, hierarchy, snapshots, views, answers, tasks, memberships, membershipHierarchy, catalogs]) => {
        const projectData = {
          project,
          hierarchy,
          snapshots,
          views,
          answers,
          tasks,
          memberships: [...memberships, ...membershipHierarchy],
          catalogs
        }

        dispatch(removeFromPending('fetchProject'))
        dispatch({ type: actionTypes.FETCH_PROJECT_SUCCESS, project: projectData })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProject'))
        dispatch({ type: actionTypes.FETCH_PROJECT_ERROR, error })
        throw error
      })
  }
}

export function createProject(data) {
  return function (dispatch) {
    dispatch(addToPending('createProject'))
    dispatch({ type: actionTypes.CREATE_PROJECT_INIT })

    return ProjectApi.createProject(data)
      .then(project => {
        dispatch(removeFromPending('createProject'))
        dispatch({ type: actionTypes.CREATE_PROJECT_SUCCESS, project })
      })
      .catch(error => {
        dispatch(removeFromPending('createProject'))
        dispatch({ type: actionTypes.CREATE_PROJECT_ERROR, error })
        throw error
      })
  }
}

export function updateProject(data) {
  return function (dispatch, getState) {
    const state = getState()
    const currentBundle = state.project?.project
    const id = data?.id ?? currentBundle?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_INIT })

    return ProjectApi.updateProject(id, data)
      .then(() =>
        Promise.all([
          ProjectApi.fetchProject(id),
          ProjectApi.fetchProjectHierarchy(id),
        ])
      )
      .then(([project, hierarchy]) => {
        const updatedBundle = {
          ...currentBundle,
          // only these two are refreshed from server:
          project,
          hierarchy,
          // everything else stays untouched:
          // snapshots: currentBundle.snapshots,
          // projectViews: currentBundle.projectViews,
          // projectAnswers: currentBundle.projectAnswers,
          // tasks: currentBundle.tasks,
          // memberships: currentBundle.memberships,
          // catalogs: currentBundle.catalogs,
        }

        dispatch(removeFromPending('updateProject'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_SUCCESS, project: updatedBundle })
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProject'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_ERROR, error })
        throw error
      })
  }
}

export function deleteProject() {
  return function (dispatch) {
    dispatch(addToPending('deleteProject'))
    dispatch({ type: actionTypes.DELETE_PROJECT_INIT })

    return ProjectApi.deleteProject(projectId)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch({ type: actionTypes.DELETE_PROJECT_SUCCESS, projectId })

        window.location.href = `${baseUrl}/projects/`
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch({ type: actionTypes.DELETE_PROJECT_ERROR, error })
        throw error
      })
  }
}

// memberships / invites / leave

export function fetchProjectInvites() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_INIT })

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_SUCCESS, invites })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_ERROR, error })
      })
  }
}

export function createProjectMember(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectMember'))
    dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_INIT })

    return ProjectApi.createMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_SUCCESS, member })
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
  }
}

export function updateProjectMember(membershipId, data) {
  return function (dispatch, getState) {
    dispatch(addToPending('updateProjectMember'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_INIT })

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_SUCCESS, member: { ...member, id: membershipId } })

        // membership updates can lead to a permission change for owner <-> last owner cases
        // project with permissions needs to be fetched
        const state = getState()
        const currentBundle = state.project.project
        return ProjectApi.fetchProject(projectId).then(project => ({ project, currentBundle }))
      })
      .then(({ project, currentBundle }) => {
        const updatedBundle = {
          ...currentBundle,
          project
        }

        dispatch(removeFromPending('updateProjectMember'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_SUCCESS, project: updatedBundle })
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectMember'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
  }
}

export function deleteProjectMember(membershipId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_INIT })

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_SUCCESS, membershipId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
  }
}

export function sendProjectInvite(data) {
  return function (dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch({ type: actionTypes.SEND_INVITE_INIT })

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch({ type: actionTypes.SEND_INVITE_SUCCESS, invite })
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch({ type: actionTypes.SEND_INVITE_ERROR, error })
        throw error
      })
  }
}

export function updateProjectInvite(inviteId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_INIT })

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_SUCCESS, invite: { ...invite, id: inviteId } })
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_ERROR, error })
        throw error
      })
  }
}

export function deleteProjectInvite(inviteId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_INIT })

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_SUCCESS, inviteId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_ERROR, error })
        throw error
      })
  }
}

export function leaveProject(membershipId, { redirect = false } = {}) {
  return function (dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch({ type: actionTypes.LEAVE_PROJECT_INIT })

    return ProjectApi.leaveProject(projectId)
      .then(() => {
        dispatch(removeFromPending('leaveProject'))
        dispatch({ type: actionTypes.LEAVE_PROJECT_SUCCESS, membershipId })
        if (redirect) {
          window.location.href = `${baseUrl}/projects/`
          return
        }
      })
      .catch(error => {
        dispatch(removeFromPending('leaveProject'))
        dispatch({ type: actionTypes.LEAVE_PROJECT_ERROR, error })
        throw error
      })
  }
}

// snapshots

export function createSnapshot(data) {
  return function (dispatch) {
    dispatch(addToPending('createSnapshot'))
    dispatch({ type: actionTypes.CREATE_SNAPSHOT_INIT })

    return ProjectApi.createSnapshot(projectId, data)
      .then(snapshot => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch({ type: actionTypes.CREATE_SNAPSHOT_SUCCESS, snapshot })
      })
      .catch(error => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch({ type: actionTypes.CREATE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function updateSnapshot(snapshotId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateSnapshot'))
    dispatch({ type: actionTypes.UPDATE_SNAPSHOT_INIT })

    return ProjectApi.updateSnapshot(projectId, snapshotId, data)
      .then(snapshot => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch({ type: actionTypes.UPDATE_SNAPSHOT_SUCCESS, snapshot })
      })
      .catch(error => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch({ type: actionTypes.UPDATE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function deleteSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('deleteSnapshot'))
    dispatch({ type: actionTypes.DELETE_SNAPSHOT_INIT })

    return ProjectApi.deleteSnapshot(projectId, snapshotId)
      .then(() => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch({ type: actionTypes.DELETE_SNAPSHOT_SUCCESS, snapshotId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch({ type: actionTypes.DELETE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function rollbackSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('rollbackSnapshot'))
    dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_INIT })

    return ProjectApi.rollbackSnapshot(projectId, snapshotId)
      .then(snapshot => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_SUCCESS, snapshot })
        dispatch(fetchProject())
      })
      .catch(error => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

// answers / views

export function fetchAnswers(snapshotId) {
  const pendingId = isNil(snapshotId) ? `fetchView/${snapshotId}` : 'fetchAnswers'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_ANSWERS_INIT })

    return ProjectApi.fetchProjectAnswers(projectId, snapshotId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_ANSWERS_SUCCESS, view })
        return view
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_ANSWERS_ERROR, error })
        throw error
      })
  }
}

export function fetchView(snapshotId, viewId) {
  const pendingId = isNil(snapshotId) ? `fetchView/${snapshotId}/${viewId}` : `fetchView/${viewId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_VIEW_INIT })

    return ProjectApi.fetchProjectView(projectId, snapshotId, viewId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_VIEW_SUCCESS, view })
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_VIEW_ERROR, error })
      })
  }
}

// download

export function downloadAnswers(snapshotId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadAnswers'))
    dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_INIT })

    return ProjectApi.downloadProjectAnswers(projectId, snapshotId, format)
      .then(() => dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_SUCCESS }))
      .catch(error => dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_ERROR, error }))
      .finally(() => dispatch(removeFromPending('downloadAnswers')))
  }
}

export function downloadView(snapshotId, viewId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadView'))
    dispatch({ type: actionTypes.DOWNLOAD_VIEW_INIT })

    return ProjectApi.downloadProjectView(projectId, snapshotId, viewId, format)
      .then(() => dispatch({ type: actionTypes.DOWNLOAD_VIEW_SUCCESS }))
      .catch(error => dispatch({ type: actionTypes.DOWNLOAD_VIEW_ERROR, error }))
      .finally(() => dispatch(removeFromPending('downloadView')))
  }
}

// synchronous actions

export function clearProjectErrors() {
  return { type: actionTypes.CLEAR_PROJECT_ERRORS }
}

export function clearCurrentView() {
  return { type: actionTypes.CLEAR_CURRENT_VIEW }
}

export function setProjectAnswers(view) {
  return function (dispatch) {
    dispatch({ type: actionTypes.SET_PROJECT_ANSWERS, view })
  }
}
