import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteQuestionModal = ({ question, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete question')} show={show} onClose={onClose} onDelete={onDelete}>
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
  </DeleteElementModal>
)

DeleteQuestionModal.propTypes = {
  question: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteQuestionModal
