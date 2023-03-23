import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteOptionModal = ({ option, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete option')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the option:')}
    </p>
    <p>
      <code className="code-options">{option.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteOptionModal.propTypes = {
  option: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteOptionModal
