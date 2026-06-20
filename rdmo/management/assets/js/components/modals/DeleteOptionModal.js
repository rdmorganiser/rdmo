import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const DeleteOptionModal = ({ option, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete option')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the option:')}
    </p>
    <p>
      <code className="code-options">{option.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteOptionModal.propTypes = {
  option: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteOptionModal
