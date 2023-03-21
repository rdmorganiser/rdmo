import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteCatalogModal = ({ catalog, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the catalog:')}
    </p>
    <p>
      <code className="code-questions">{catalog.uri}</code>
    </p>
    <p dangerouslySetInnerHTML={{
      __html: interpolate(ngettext(
        'This catalog is used in <b>one project</b>, which will not be usable afterwards.',
        'This catalog is used in <b>%s projects</b>, which will not be usable afterwards.',
        catalog.projects_count
      ), [catalog.projects_count])}} />
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteCatalogModal.propTypes = {
  catalog: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteCatalogModal
