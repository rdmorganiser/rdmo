import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

import { projectId } from '../utils/meta'

import ContactApi from '../api/ContactApi'

import {
  CLOSE_CONTACT,
  FETCH_CONTACT_ERROR,
  FETCH_CONTACT_INIT,
  FETCH_CONTACT_SUCCESS,
  SEND_CONTACT_ERROR,
  SEND_CONTACT_INIT,
  SEND_CONTACT_SUCCESS
} from './actionTypes'

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
    dispatch({type: FETCH_CONTACT_INIT})

    return ContactApi.fetchContact(projectId, params)
      .then((values) => dispatch({type: FETCH_CONTACT_SUCCESS, values}))
      .catch((error) => dispatch({type: FETCH_CONTACT_ERROR, error}))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function sendContact(values) {
  const pendingId = 'sendContact'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch({type: SEND_CONTACT_INIT})

    return ContactApi.sendContact(projectId, values)
      .then(() => dispatch({type: SEND_CONTACT_SUCCESS}))
      .catch((error) => dispatch({type: SEND_CONTACT_ERROR, error}))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function closeContact() {
  return {type: CLOSE_CONTACT}
}
