import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeletePageModal = ({ page, sections, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete page')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the page:')}
    </p>
    <p>
      <code className="code-questions">{page.uri}</code>
    </p>
    {
      sections.length > 0 && <>
        <p>
          {gettext('This page is used in the following sections, from which it will be removed:')}
        </p>
        {
          sections.map((section, index) => (
            <p key={index}>
              <code className="code-questions">{section.uri}</code>
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

DeletePageModal.propTypes = {
  page: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeletePageModal
