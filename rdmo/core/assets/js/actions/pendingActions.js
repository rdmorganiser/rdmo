import { ADD_TO_PENDING, REMOVE_FROM_PENDING } from './actionTypes'

export function addToPending(item) {
  return {type: ADD_TO_PENDING, item}
}

export function removeFromPending(item) {
  return {type: REMOVE_FROM_PENDING, item}
}
