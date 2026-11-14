import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions as projectActions } from '../reducers/projectSlice'
import { actions } from '../reducers/snapshotSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProjectSnapshots() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectSnapshots'))
    dispatch(projectActions.fetchProjectSnapshotsInit())

    return ProjectApi.fetchProjectSnapshots(projectId)
      .then(snapshots => {
        dispatch(actions.fetchProjectSnapshotsSuccess(snapshots))
        return snapshots
      })
      .catch(error => {
        dispatch(projectActions.fetchProjectSnapshotsError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectSnapshots')))
  }
}

export function createSnapshot(data) {
  return function (dispatch) {
    dispatch(addToPending('createSnapshot'))
    dispatch(projectActions.createSnapshotInit())

    return ProjectApi.createSnapshot(projectId, data)
      .then(snapshot => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch(actions.createSnapshotSuccess(snapshot))
      })
      .catch(error => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch(projectActions.createSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function updateSnapshot(snapshotId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateSnapshot'))
    dispatch(projectActions.updateSnapshotInit())

    return ProjectApi.updateSnapshot(projectId, snapshotId, data)
      .then(snapshot => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch(actions.updateSnapshotSuccess(snapshot))
      })
      .catch(error => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch(projectActions.updateSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function deleteSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('deleteSnapshot'))
    dispatch(projectActions.deleteSnapshotInit())

    return ProjectApi.deleteSnapshot(projectId, snapshotId)
      .then(() => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch(actions.deleteSnapshotSuccess(snapshotId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch(projectActions.deleteSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function rollbackSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('rollbackSnapshot'))
    dispatch(projectActions.rollbackSnapshotInit())

    return ProjectApi.rollbackSnapshot(projectId, snapshotId)
      .then(() =>
        Promise.all([
          ProjectApi.fetchProject(projectId),
          ProjectApi.fetchProjectSnapshots(projectId)
        ])
      )
      .then(([project, snapshots]) => {
        dispatch(actions.rollbackSnapshotSuccess(snapshots))
        dispatch(projectActions.updateProjectSuccess({ project }))
      })
      .catch(error => {
        dispatch(projectActions.rollbackSnapshotError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('rollbackSnapshot')))
  }
}
