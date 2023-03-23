import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteConditionModal = ({ condition, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete condition')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the condition:')}
    </p>
    <p>
      <code className="code-conditions">{condition.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteConditionModal.propTypes = {
  condition: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteConditionModal
