import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const DeleteConditionModal = ({ condition, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete condition')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the condition:')}
    </p>
    <p>
      <code className="code-conditions">{condition.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteConditionModal.propTypes = {
  condition: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteConditionModal
