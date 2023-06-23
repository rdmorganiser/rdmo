import React from 'react'
import PropTypes from 'prop-types'

import { DeleteModal } from '../common/Modals'

const DeleteQuestionModal = ({ question, info, show, onClose, onDelete }) => (
  <DeleteModal title={gettext('Delete question')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the question:')}
    </p>
    <p>
      <code className="code-questions">{question.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteModal>
)

DeleteQuestionModal.propTypes = {
  question: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteQuestionModal
