import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const DeleteSectionModal = ({ section, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete section')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the section:')}
    </p>
    <p>
      <code className="code-questions">{section.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteSectionModal.propTypes = {
  section: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteSectionModal
