import ProjectApi from '../api/ProjectApi'
import CatalogsApi from '/rdmo/projects/assets/js/common/api/CatalogsApi'

import { projectId } from '../utils/meta'
import * as actionTypes from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { updateLocation } from '../utils/location'

export function setPage(page) {
  return function(dispatch) {
    dispatch(updateConfig('page', page))
    updateLocation(page)
  }
}

export function fetchProject() {
  return function(dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch(fetchProjectInit())

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      CatalogsApi.fetchCatalogs()
    ])
    .then(([project, snapshots, tasks, memberships, catalogs]) => {
      const projectData = {
        project: project,
        snapshots: snapshots,
        tasks: tasks,
        memberships: memberships,
        catalogs: catalogs
      }

      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectSuccess(projectData))
    })
    .catch(error => {
      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectError(error))
      throw error
    })
  }
}

export function fetchProjectInit() {
  return { type: actionTypes.FETCH_PROJECT_INIT }
}

export function fetchProjectSuccess(project) {
  return { type: actionTypes.FETCH_PROJECT_SUCCESS, project }
}

export function fetchProjectError(error) {
  return { type: actionTypes.FETCH_PROJECT_ERROR, error }
}

export function updateProject(data) {
  return function(dispatch, getState) {
    const state = getState()
    const currentBundle = state.project.project
    const id = currentBundle?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch(updateProjectInit())

    return ProjectApi.updateProject(id, data)
      .then((updatedProject) => {
        const updatedBundle = {
          ...currentBundle,
          project: updatedProject
        }

        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectSuccess(updatedBundle))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectError(error))
        throw error
      })
  }
}

export function updateProjectInit() {
  return { type: actionTypes.UPDATE_PROJECT_INIT }
}

export function updateProjectSuccess(project) {
  return { type: actionTypes.UPDATE_PROJECT_SUCCESS, project }
}

export function updateProjectError(error) {
  return { type: actionTypes.UPDATE_PROJECT_ERROR, error }
}

export function deleteProject(projectId) {
  return function(dispatch) {
    dispatch(addToPending('deleteProject'))
    dispatch(deleteProjectInit())

    return ProjectApi.deleteProject(projectId)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectSuccess(projectId))
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectError(error))
        throw error
      })
  }
}

export function deleteProjectInit() {
  return { type: actionTypes.DELETE_PROJECT_INIT }
}

export function deleteProjectSuccess(projectId) {
  return { type: actionTypes.DELETE_PROJECT_SUCCESS, projectId }
}

export function deleteProjectError(error) {
  return { type: actionTypes.DELETE_PROJECT_ERROR, error }
}

export function fetchProjectInvites() {
  return function(dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch(fetchProjectInvitesInit())

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(fetchProjectInvitesSuccess(invites))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(fetchProjectInvitesError(error))
      })
  }
}

export function fetchProjectInvitesInit() {
  return { type: actionTypes.FETCH_PROJECT_INVITES_INIT }
}

export function fetchProjectInvitesSuccess(invites) {
  return { type: actionTypes.FETCH_PROJECT_INVITES_SUCCESS, invites }
}

export function fetchProjectInvitesError(error) {
  return { type: actionTypes.FETCH_PROJECT_INVITES_ERROR, error }
}

export function addProjectMember(data) {
  return function(dispatch) {
    dispatch(addToPending('addProjectMember'))
    dispatch(addProjectMemberInit())

    return ProjectApi.addMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('addProjectMember'))
        dispatch(addProjectMemberSuccess(member))
        return dispatch(refreshProjectCore())
      })
      .catch(error => {
        dispatch(removeFromPending('addProjectMember'))
        dispatch(addProjectMemberError(error))
        throw error
      })
  }
}

export function addProjectMemberInit() {
  return { type: actionTypes.ADD_PROJECT_MEMBER_INIT }
}

export function addProjectMemberSuccess(member) {
  return { type: actionTypes.ADD_PROJECT_MEMBER_SUCCESS, member }
}

export function addProjectMemberError(error) {
  return { type: actionTypes.ADD_PROJECT_MEMBER_ERROR, error }
}

export function editProjectMember(membershipId, data) {
  return function(dispatch) {
    dispatch(addToPending('editProjectMember'))
    dispatch(editProjectMemberInit())

    return ProjectApi.editMember(projectId, membershipId, data)
      .then(member => {
        dispatch(removeFromPending('editProjectMember'))
        dispatch(editProjectMemberSuccess(member))
        return dispatch(refreshProjectCore())
      })
      .catch(error => {
        dispatch(removeFromPending('editProjectMember'))
        dispatch(editProjectMemberError(error))
        throw error
      })
  }
}

export function editProjectMemberInit() {
  return { type: actionTypes.EDIT_PROJECT_MEMBER_INIT }
}

export function editProjectMemberSuccess(member) {
  return { type: actionTypes.EDIT_PROJECT_MEMBER_SUCCESS, member }
}

export function editProjectMemberError(error) {
  return { type: actionTypes.EDIT_PROJECT_MEMBER_ERROR, error }
}

export function deleteProjectMember(membershipId, { skipRefresh = false } = {}) {
  return function(dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch(deleteProjectMemberInit())

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(deleteProjectMemberSuccess(membershipId))
        if (skipRefresh) {
          window.location.href = '/projects/'
          return
        }
        return dispatch(refreshProjectCore())
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(deleteProjectMemberError(error))
        throw error
      })
  }
}

export function deleteProjectMemberInit() {
  return { type: actionTypes.DELETE_PROJECT_MEMBER_INIT }
}

export function deleteProjectMemberSuccess(membershipId) {
  return { type: actionTypes.DELETE_PROJECT_MEMBER_SUCCESS, membershipId }
}

export function deleteProjectMemberError(error) {
  return { type: actionTypes.DELETE_PROJECT_MEMBER_ERROR, error }
}

export function sendProjectInvite(data) {
  return function(dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch(sendProjectInviteInit())

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(sendProjectInviteSuccess(invite))
        return dispatch(fetchProjectInvites())
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(sendProjectInviteError(error))
        throw error
      })
  }
}

export function sendProjectInviteInit() {
  return { type: actionTypes.SEND_INVITE_INIT }
}

export function sendProjectInviteSuccess(invite) {
  return { type: actionTypes.SEND_INVITE_SUCCESS, invite }
}

export function sendProjectInviteError(error) {
  return { type: actionTypes.SEND_INVITE_ERROR, error }
}

export function editProjectInvite(inviteId, data) {
  return function(dispatch) {
    dispatch(addToPending('editProjectInvite'))
    dispatch(editProjectInviteInit())

    return ProjectApi.editInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('editProjectInvite'))
        dispatch(editProjectInviteSuccess(invite))
        return dispatch(fetchProjectInvites())
      })
      .catch(error => {
        dispatch(removeFromPending('editProjectInvite'))
        dispatch(editProjectInviteError(error))
        throw error
      })
  }
}

export function editProjectInviteInit() {
  return { type: actionTypes.EDIT_PROJECT_INVITE_INIT }
}

export function editProjectInviteSuccess(invite) {
  return { type: actionTypes.EDIT_PROJECT_INVITE_SUCCESS, invite }
}

export function editProjectInviteError(error) {
  return { type: actionTypes.EDIT_PROJECT_INVITE_ERROR, error }
}

export function deleteProjectInvite(inviteId) {
  return function(dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch(deleteProjectInviteInit())

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(deleteProjectInviteSuccess(inviteId))
        return dispatch(fetchProjectInvites())
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(deleteProjectInviteError(error))
        throw error
      })
  }
}

export function deleteProjectInviteInit() {
  return { type: actionTypes.DELETE_PROJECT_INVITE_INIT }
}

export function deleteProjectInviteSuccess(inviteId) {
  return { type: actionTypes.DELETE_PROJECT_INVITE_SUCCESS, inviteId }
}

export function deleteProjectInviteError(error) {
  return { type: actionTypes.DELETE_PROJECT_INVITE_ERROR, error }
}

export function refreshProjectCore() {
  return function(dispatch) {
    dispatch(addToPending('refreshProjectCore'))
    dispatch({ type: actionTypes.REFRESH_PROJECT_CORE_INIT })

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectMemberships(projectId)
    ])
    .then(([projectEntity, memberships]) => {
      dispatch(removeFromPending('refreshProjectCore'))
      dispatch({
        type: actionTypes.REFRESH_PROJECT_CORE_SUCCESS,
        project: projectEntity,
        memberships
      })
    })
    .catch((error) => {
      dispatch(removeFromPending('refreshProjectCore'))
      dispatch({ type: actionTypes.REFRESH_PROJECT_CORE_ERROR, error })
      throw error
    })
  }
}
