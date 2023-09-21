import React from 'react'
import PropTypes from 'prop-types'

import { DeleteModal } from '../common/Modals'

const DeleteAttributeModal = ({ attribute, info, show, onClose, onDelete }) => (
  <DeleteModal title={gettext('Delete attribute')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the attribute:')}
    </p>
    <p>
      <code className="code-domain">{attribute.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteModal>
)

DeleteAttributeModal.propTypes = {
  attribute: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteAttributeModal
