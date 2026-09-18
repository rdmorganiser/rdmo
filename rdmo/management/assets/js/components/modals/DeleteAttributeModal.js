import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const DeleteAttributeModal = ({ attribute, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete attribute')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the attribute:')}
    </p>
    <p>
      <code className="code-domain">{attribute.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteAttributeModal.propTypes = {
  attribute: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteAttributeModal
