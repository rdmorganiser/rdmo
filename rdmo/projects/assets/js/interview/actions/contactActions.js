import ContactApi from '../api/ContactApi'

import { projectId } from '../utils/meta'

import {
  FETCH_CONTACT_INIT,
  FETCH_CONTACT_SUCCESS,
  FETCH_CONTACT_ERROR,
  SEND_CONTACT_INIT,
  SEND_CONTACT_SUCCESS,
  SEND_CONTACT_ERROR,
  CLOSE_CONTACT
} from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

export function fetchContact({ questionset, question, values }) {
  const pendingId = 'fetchContact'

  return (dispatch, getState) => {
    const params = {
      page: getState().interview.page.id,
      questionset: questionset && questionset.id,
      question: question && question.id,
      values: values.filter(value => value.id).map(value => value.id)
    }

    dispatch(addToPending(pendingId))
    dispatch(fetchContactInit())

    return ContactApi.fetchContact(projectId, params).then((values) => {
      dispatch(removeFromPending(pendingId))
      dispatch(fetchContactSuccess(values))
    }).catch((error) => {
      dispatch(removeFromPending(pendingId))
      dispatch(fetchContactError(error))
    })
  }
}

export function fetchContactInit() {
  return {type: FETCH_CONTACT_INIT}
}

export function fetchContactSuccess(values) {
  return {type: FETCH_CONTACT_SUCCESS, values}
}

export function fetchContactError(error) {
  return {type: FETCH_CONTACT_ERROR, error}
}

export function sendContact(values) {
  const pendingId = 'sendContact'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(sendContactInit())

    return ContactApi.sendContact(projectId, values).then(() => {
      dispatch(removeFromPending(pendingId))
      dispatch(sendContactSuccess())
    }).catch((error) => {
      dispatch(removeFromPending(pendingId))
      dispatch(sendContactError(error))
    })
  }
}

export function sendContactInit() {
  return {type: SEND_CONTACT_INIT}
}

export function sendContactSuccess() {
  return {type: SEND_CONTACT_SUCCESS}
}

export function sendContactError(error) {
  return {type: SEND_CONTACT_ERROR, error}
}

export function closeContact() {
  return {type: CLOSE_CONTACT}
}
