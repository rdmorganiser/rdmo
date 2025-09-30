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
      ProjectApi.fetchProjectHierarchy(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      ProjectApi.fetchProjectMembershipHierarchy(projectId),
      CatalogsApi.fetchCatalogs()
    ])
    .then(([project, hierarchy, snapshots, tasks, memberships, membershipHierarchy, catalogs]) => {
      const projectData = {
        project: project,
        hierarchy: hierarchy,
        snapshots: snapshots,
        tasks: tasks,
        memberships: [...memberships, ...membershipHierarchy],
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
          // tasks: currentBundle.tasks,
          // memberships: currentBundle.memberships,
          // catalogs: currentBundle.catalogs,
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

export function deleteProject() {
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

export function createProjectMember(data) {
  return function(dispatch) {
    dispatch(addToPending('createProjectMember'))
    dispatch(createProjectMemberInit())

    return ProjectApi.createMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(createProjectMemberSuccess(member))
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(createProjectMemberError(error))
        throw error
      })
  }
}

export function createProjectMemberInit() {
  return { type: actionTypes.CREATE_PROJECT_MEMBER_INIT }
}

export function createProjectMemberSuccess(member) {
  return { type: actionTypes.CREATE_PROJECT_MEMBER_SUCCESS, member }
}

export function createProjectMemberError(error) {
  return { type: actionTypes.CREATE_PROJECT_MEMBER_ERROR, error }
}

export function updateProjectMember(membershipId, data) {
  return function(dispatch) {
    dispatch(addToPending('updateProjectMember'))
    dispatch(updateProjectMemberInit())

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        dispatch(removeFromPending('updateProjectMember'))
        dispatch(updateProjectMemberSuccess({ ...member, id: membershipId }))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectMember'))
        dispatch(updateProjectMemberError(error))
        throw error
      })
  }
}

export function updateProjectMemberInit() {
  return { type: actionTypes.UPDATE_PROJECT_MEMBER_INIT }
}

export function updateProjectMemberSuccess(member) {
  return { type: actionTypes.UPDATE_PROJECT_MEMBER_SUCCESS, member }
}

export function updateProjectMemberError(error) {
  return { type: actionTypes.UPDATE_PROJECT_MEMBER_ERROR, error }
}

export function deleteProjectMember(membershipId) {
  return function(dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch(deleteProjectMemberInit())

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(deleteProjectMemberSuccess(membershipId))
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

export function updateProjectInvite(inviteId, data) {
  return function(dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch(updateProjectInviteInit())

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(updateProjectInviteSuccess({...invite, id: inviteId}))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(updateProjectInviteError(error))
        throw error
      })
  }
}

export function updateProjectInviteInit() {
  return { type: actionTypes.UPDATE_PROJECT_INVITE_INIT }
}

export function updateProjectInviteSuccess(invite) {
  return { type: actionTypes.UPDATE_PROJECT_INVITE_SUCCESS, invite }
}

export function updateProjectInviteError(error) {
  return { type: actionTypes.UPDATE_PROJECT_INVITE_ERROR, error }
}

export function deleteProjectInvite(inviteId) {
  return function(dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch(deleteProjectInviteInit())

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(deleteProjectInviteSuccess(inviteId))
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

export function leaveProject(membershipId, { redirect = false } = {}) {
  return function(dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch(leaveProjectInit())

    return ProjectApi.leaveProject(projectId)
    .then(() => {
      dispatch(removeFromPending('leaveProject'))
      dispatch(leaveProjectSuccess(membershipId))
      if (redirect) {
        window.location.href = '/projects/'
        return
      }
    })
    .catch(error => {
      dispatch(removeFromPending('leaveProject'))
      dispatch(leaveProjectError(error))
      throw error
    })
  }
}

export function leaveProjectInit() {
  return { type: actionTypes.LEAVE_PROJECT_INIT }
}

export function leaveProjectSuccess(membershipId) {
  return { type: actionTypes.LEAVE_PROJECT_SUCCESS, membershipId }
}

export function leaveProjectError(error) {
  return { type: actionTypes.LEAVE_PROJECT_ERROR, error }
}

export function clearProjectErrors() {
  return { type: actionTypes.CLEAR_PROJECT_ERRORS }
}
