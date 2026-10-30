import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Html, Modal } from 'rdmo/core/assets/js/components'

import { hideDone } from '../../../actions/interviewActions'
import { navigateDashboard } from '../../../actions/navigationActions'

const InterviewDone = () => {
  const dispatch = useDispatch()
  const { done } = useSelector((state) => state.interview)
  const templates = useSelector((state) => state.templates)

  const onSubmit = () => {
    dispatch(hideDone())
    dispatch(navigateDashboard({area: 'documents'}))
  }

  const onClose = () => dispatch(hideDone())

  const submitLabel = (
    <span className="d-inline-flex align-items-center gap-2">
      {gettext('To Documents')} <i className="bi bi-arrow-right"></i>
    </span>
  )

  return (
    <Modal
      title={gettext('Done')}
      show={done}
      submitLabel={submitLabel}
      onSubmit={onSubmit}
      onClose={onClose}
      size="modal-lg"
    >
      <Html html={templates.project_interview_done} />
    </Modal>
  )
}

export default InterviewDone
