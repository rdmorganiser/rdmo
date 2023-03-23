import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteQuestionSetModal = ({ questionset, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete question set')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the question set:')}
    </p>
    <p>
      <code className="code-questions">{questionset.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteQuestionSetModal.propTypes = {
  questionset: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteQuestionSetModal
