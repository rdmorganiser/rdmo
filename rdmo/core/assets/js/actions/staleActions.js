import { actions } from '../reducers/staleSlice'

export function addToStale(item) {
  return actions.addToStale(item)
}

export function removeFromStale(item) {
  return actions.removeFromStale(item)
}
