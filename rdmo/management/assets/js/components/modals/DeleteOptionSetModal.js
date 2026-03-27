import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const DeleteOptionSetModal = ({ optionset, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete optionset')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the option set:')}
    </p>
    <p>
      <code className="code-options">{optionset.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteOptionSetModal.propTypes = {
  optionset: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteOptionSetModal
