import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { actions } from '../reducers/membershipSlice'
import { actions as projectActions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProjectMemberships() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectMemberships'))
    dispatch(projectActions.fetchProjectMembershipsInit())

    return Promise.all([
      ProjectApi.fetchProjectMemberships(projectId),
      ProjectApi.fetchProjectMembershipHierarchy(projectId)
    ])
      .then(([memberships, membershipHierarchy]) => {
        const allMemberships = [...memberships, ...membershipHierarchy]
        dispatch(actions.fetchProjectMembershipsSuccess(allMemberships))
        return allMemberships
      })
      .catch(error => {
        dispatch(projectActions.fetchProjectMembershipsError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectMemberships')))
  }
}

export function fetchProjectInvites() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch(projectActions.fetchProjectInvitesInit())

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(actions.fetchProjectInvitesSuccess(invites))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(projectActions.fetchProjectInvitesError(serializeError(error)))
      })
  }
}

export function createProjectMember(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectMember'))
    dispatch(projectActions.createProjectMemberInit())

    return ProjectApi.createMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(actions.createProjectMemberSuccess(member))
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(projectActions.createProjectMemberError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectMember(membershipId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectMember'))
    dispatch(projectActions.updateProjectMemberInit())

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        // membership updates can lead to a permission change for owner <-> last owner cases
        // project with permissions needs to be fetched
        return ProjectApi.fetchProject(projectId)
          .then(project => {
            dispatch(actions.updateProjectMemberSuccess({ ...member, id: membershipId }))
            dispatch(projectActions.updateProjectSuccess({ project }))
          })
      })
      .catch(error => {
        dispatch(projectActions.updateProjectMemberError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectMember')))
  }
}

export function deleteProjectMember(membershipId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch(projectActions.deleteProjectMemberInit())

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(actions.deleteProjectMemberSuccess(membershipId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(projectActions.deleteProjectMemberError(serializeError(error)))
        throw error
      })
  }
}

export function sendProjectInvite(data) {
  return function (dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch(projectActions.sendInviteInit())

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(actions.sendInviteSuccess(invite))
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(projectActions.sendInviteError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectInvite(inviteId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch(projectActions.updateProjectInviteInit())

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(actions.updateProjectInviteSuccess({ ...invite, id: inviteId }))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(projectActions.updateProjectInviteError(serializeError(error)))
        throw error
      })
  }
}

export function deleteProjectInvite(inviteId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch(projectActions.deleteProjectInviteInit())

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(actions.deleteProjectInviteSuccess(inviteId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(projectActions.deleteProjectInviteError(serializeError(error)))
        throw error
      })
  }
}

export function leaveProject(membershipId, { redirect = false } = {}) {
  return function (dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch(projectActions.leaveProjectInit())

    return ProjectApi.leaveProject(projectId)
      .then(() => {
        dispatch(removeFromPending('leaveProject'))
        dispatch(actions.leaveProjectSuccess(membershipId))
        if (redirect) {
          window.location.href = `${baseUrl}/projects/`
          return
        }
      })
      .catch(error => {
        dispatch(removeFromPending('leaveProject'))
        dispatch(projectActions.leaveProjectError(serializeError(error)))
        throw error
      })
  }
}
