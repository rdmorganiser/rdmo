import React from 'react'
import PropTypes from 'prop-types'

import { DeleteModal } from '../common/Modals'

const DeleteTaskModal = ({ task, info, show, onClose, onDelete }) => (
  <DeleteModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the task:')}
    </p>
    <p>
      <code className="code-tasks">{task.uri}</code>
    </p>
    { info }
    <p className="text-danger">
      {gettext('The task will be removed from these projects.')} {gettext('This action cannot be undone!')}
    </p>
  </DeleteModal>
)

DeleteTaskModal.propTypes = {
  task: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteTaskModal
