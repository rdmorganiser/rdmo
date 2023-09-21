import React from 'react'
import PropTypes from 'prop-types'

import { DeleteModal } from '../common/Modals'

const DeleteViewModal = ({ view, info, show, onClose, onDelete }) => (
  <DeleteModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
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
  </DeleteModal>
)

DeleteViewModal.propTypes = {
  view: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteViewModal
