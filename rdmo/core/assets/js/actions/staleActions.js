import { ADD_TO_STALE, REMOVE_FROM_STALE } from './actionTypes'

export function addToStale(item) {
  return {type: ADD_TO_STALE, item}
}

export function removeFromStale(item) {
  return {type: REMOVE_FROM_STALE, item}
}
