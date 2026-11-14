import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/contactSlice'
import { projectId } from '../utils/meta'

import ContactApi from '../api/ContactApi'

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
    dispatch(actions.fetchContactInit())

    return ContactApi.fetchContact(projectId, params)
      .then((values) => dispatch(actions.fetchContactSuccess(values)))
      .catch((error) => dispatch(actions.fetchContactError(serializeError(error))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function sendContact(values) {
  const pendingId = 'sendContact'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.sendContactInit())

    return ContactApi.sendContact(projectId, values)
      .then(() => dispatch(actions.sendContactSuccess()))
      .catch((error) => dispatch(actions.sendContactError(serializeError(error))))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function closeContact() {
  return actions.closeContact()
}
