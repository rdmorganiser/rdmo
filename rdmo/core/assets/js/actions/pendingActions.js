import { actions } from '../reducers/pendingSlice'

export function addToPending(item) {
  return actions.addToPending(item)
}

export function removeFromPending(item) {
  return actions.removeFromPending(item)
}
