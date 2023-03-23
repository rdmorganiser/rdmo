import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteSectionModal = ({ section, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete section')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the section:')}
    </p>
    <p>
      <code className="code-questions">{section.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteSectionModal.propTypes = {
  section: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteSectionModal
