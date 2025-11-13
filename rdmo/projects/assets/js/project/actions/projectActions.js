import CatalogsApi from 'rdmo/projects/assets/js/common/api/CatalogsApi'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { projectId } from '../utils/meta'
import { updateLocation } from '../utils/location'

import ProjectApi from '../api/ProjectApi'
import ViewsApi from '../api/ViewsApi'

import * as actionTypes from './actionTypes'

export function setPage(page) {
  return function (dispatch) {
    dispatch(updateConfig('page', page))
    updateLocation(page)
  }
}

export function fetchProject() {
  return function (dispatch) {
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
  return function (dispatch, getState) {
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
  return function (dispatch) {
    dispatch(addToPending('deleteProject'))
    dispatch(deleteProjectInit())

    return ProjectApi.deleteProject(projectId)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectSuccess(projectId))

        window.location.href = `${baseUrl}/projects/`
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
  return function (dispatch) {
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
  return function (dispatch) {
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
  return function (dispatch, getState) {
    dispatch(addToPending('updateProjectMember'))
    dispatch(updateProjectMemberInit())

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        dispatch(updateProjectMemberSuccess({ ...member, id: membershipId }))

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
        dispatch(updateProjectSuccess(updatedBundle))
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
  return function (dispatch) {
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
  return function (dispatch) {
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
  return function (dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch(updateProjectInviteInit())

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(updateProjectInviteSuccess({ ...invite, id: inviteId }))
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
  return function (dispatch) {
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
  return function (dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch(leaveProjectInit())

    return ProjectApi.leaveProject(projectId)
      .then(() => {
        dispatch(removeFromPending('leaveProject'))
        dispatch(leaveProjectSuccess(membershipId))
        if (redirect) {
          window.location.href = `${baseUrl}/projects/`
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

export function rollbackSnapshot(snapshotId, data) {
  return function (dispatch) {
    dispatch(addToPending('rollbackSnapshot'))
    dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_INIT })

    return ProjectApi.rollbackSnapshot(projectId, snapshotId, data)
      .then(snapshot => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_SUCCESS, snapshot })
      })
      .catch(error => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function fetchProjectViews(viewIds) {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectViews'))
    dispatch(fetchProjectViewsInit())

    return Promise.all(viewIds.map(id => ViewsApi.fetchView(id)))
      .then(projectViews => {
        dispatch(removeFromPending('fetchProjectViews'))
        dispatch(fetchProjectViewsSuccess(projectViews))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectViews'))
        dispatch(fetchProjectViewsError(error))
        throw error
      })
  }
}

export function fetchProjectViewsInit() {
  return { type: actionTypes.FETCH_PROJECT_VIEWS_INIT }
}

export function fetchProjectViewsSuccess(projectViews) {
  return { type: actionTypes.FETCH_PROJECT_VIEWS_SUCCESS, projectViews }
}

export function fetchProjectViewsError(error) {
  return { type: actionTypes.FETCH_PROJECT_VIEWS_ERROR, error }
}
