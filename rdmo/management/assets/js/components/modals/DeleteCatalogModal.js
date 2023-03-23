import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteCatalogModal = ({ catalog, info, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the catalog:')}
    </p>
    <p>
      <code className="code-questions">{catalog.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('Those projects will not be usable afterwards.')} {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteCatalogModal.propTypes = {
  catalog: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteCatalogModal
