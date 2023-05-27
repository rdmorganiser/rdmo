import React from 'react'
import PropTypes from 'prop-types'

import { DeleteModal } from '../common/Modals'

const DeletePageModal = ({ page, info, show, onClose, onDelete }) => (
  <DeleteModal title={gettext('Delete page')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the page:')}
    </p>
    <p>
      <code className="code-questions">{page.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteModal>
)

DeletePageModal.propTypes = {
  page: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeletePageModal
