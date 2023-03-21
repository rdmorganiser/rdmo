import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteViewModal = ({ view, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the view:')}
    </p>
    <p>
      <code className="code-views">{view.uri}</code>
    </p>
    <p dangerouslySetInnerHTML={{
      __html: interpolate(ngettext(
        'This task is used in <b>one project</b>, from which it will be removed.',
        'This task is used in <b>%s projects</b>, from which it will be removed.',
        view.projects_count
      ), [view.projects_count])}} />
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteViewModal.propTypes = {
  view: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteViewModal
