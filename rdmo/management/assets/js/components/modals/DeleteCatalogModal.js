import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const DeleteCatalogModal = ({ catalog, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete catalog')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the catalog:')}
    </p>
    <p>
      <code className="code-questions">{catalog.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('Those projects will not be usable afterwards.')} {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteCatalogModal.propTypes = {
  catalog: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteCatalogModal
