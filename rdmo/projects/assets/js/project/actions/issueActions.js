import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { addToStale } from 'rdmo/core/assets/js/actions/staleActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/issueSlice'
import { actions as projectActions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProjectIssues() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectIssues'))
    dispatch(projectActions.fetchProjectIssuesInit())

    return ProjectApi.fetchProjectIssues(projectId)
      .then((issues) => {
        dispatch(actions.fetchProjectIssuesSuccess(issues))
      })
      .catch((error) => {
        dispatch(projectActions.fetchProjectIssuesError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectIssues')))
  }
}

export function updateProjectIssue(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectIssue'))
    dispatch(projectActions.updateProjectIssueInit())

    return ProjectApi.updateProjectIssue(projectId, issueId, data)
      .then(() => dispatch(fetchProjectIssues()))
      .then(() => {
        dispatch(actions.updateProjectIssueSuccess())
      })
      .catch((error) => {
        dispatch(projectActions.updateProjectIssueError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectIssue')))
  }
}

export function sendProjectIssueEmail(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueEmail'))
    dispatch(projectActions.sendProjectIssueEmailInit())

    return ProjectApi.sendProjectIssueEmail(projectId, issueId, data)
      .then(() => {
        dispatch(actions.sendProjectIssueEmailSuccess())

        return dispatch(fetchProjectIssues())
          .catch(() => {})
      }, error => {
        dispatch(projectActions.sendProjectIssueEmailError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueEmail')))
  }
}

export function sendProjectIssueIntegration(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueIntegration'))
    dispatch(projectActions.sendProjectIssueIntegrationInit())

    return ProjectApi.sendProjectIssueIntegration(projectId, issueId, data)
      .then((response) => {
        dispatch(actions.sendProjectIssueIntegrationSuccess())

        if (response?.redirect_url) {
          dispatch(addToStale('projectIssues'))
          window.location.href = response.redirect_url
          return response
        }

        return dispatch(fetchProjectIssues())
          .catch(() => {})
          .then(() => response)
      }, error => {
        dispatch(projectActions.sendProjectIssueIntegrationError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueIntegration')))
  }
}
