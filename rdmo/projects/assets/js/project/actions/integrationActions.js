import * as errorActions from 'rdmo/core/assets/js/actions/errorsActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/integrationSlice'
import { actions as projectActions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProviders() {
  return function (dispatch) {
    dispatch(addToPending('fetchProviders'))
    dispatch(errorActions.clearError('integrationProviders'))

    return ProjectApi.fetchProviders()
      .then(providers => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch(actions.fetchProvidersSuccess(providers))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch(errorActions.setError('integrationProviders', error, gettext('Integration providers')))
        throw error
      })
  }
}

export function fetchProjectIntegrations() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectIntegrations'))
    dispatch(projectActions.fetchProjectIntegrationsInit())

    return ProjectApi.fetchProjectIntegrations(projectId)
      .then(integrations => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch(actions.fetchProjectIntegrationsSuccess(integrations))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch(projectActions.fetchProjectIntegrationsError(serializeError(error)))
        throw error
      })
  }
}

export function createProjectIntegration(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectIntegration'))
    dispatch(projectActions.createProjectIntegrationInit())

    return ProjectApi.createProjectIntegration(projectId, data)
      .then(integration => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch(actions.createProjectIntegrationSuccess(integration))
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch(projectActions.createProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectIntegration(integrationId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectIntegration'))
    dispatch(projectActions.updateProjectIntegrationInit())

    return ProjectApi.updateProjectIntegration(projectId, integrationId, data)
      .then(integration => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch(actions.updateProjectIntegrationSuccess(integration))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch(projectActions.updateProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}

export function deleteProjectIntegration(integrationId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectIntegration'))
    dispatch(projectActions.deleteProjectIntegrationInit())

    return ProjectApi.deleteProjectIntegration(projectId, integrationId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch(actions.deleteProjectIntegrationSuccess(integrationId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch(projectActions.deleteProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}
