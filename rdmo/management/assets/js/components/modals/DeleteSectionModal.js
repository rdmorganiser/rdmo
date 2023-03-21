import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteSectionModal = ({ section, catalogs, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete section')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the section:')}
    </p>
    <p>
      <code className="code-questions">{section.uri}</code>
    </p>
    {
      catalogs.length > 0 && <>
        <p>
          <strong>{gettext('Important!')}</strong>
        </p>
        <p>
          {gettext('This section is used in the following catalogs, from which it will be removed:')}
        </p>
        {
          catalogs.map((catalog, index) => (
            <p key={index}>
              <code className="code-questions">{catalog.uri}</code>
            </p>
          ))
        }
      </>
    }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteSectionModal.propTypes = {
  section: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteSectionModal
