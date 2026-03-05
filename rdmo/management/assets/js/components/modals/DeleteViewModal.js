import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const DeleteViewModal = ({ view, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete view')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the view:')}
    </p>
    <p>
      <code className="code-views">{view.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('The view will be removed from these projects.')} {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteViewModal.propTypes = {
  view: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteViewModal
