import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const DeleteTaskModal = ({ task, info, show, onClose, onDelete }) => (
  <Modal
    title={gettext('Delete task')}
    show={show}
    onClose={onClose}
    onSubmit={onDelete}
    submitLabel={gettext('Delete')}
    submitProps={{ className: 'btn btn-danger' }}
    size="modal-lg"
  >
    <p>
      {gettext('You are about to permanently delete the task:')}
    </p>
    <p>
      <code className="code-tasks">{task.uri}</code>
    </p>
    {info}
    <p className="text-danger">
      {gettext('The task will be removed from these projects.')} {gettext('This action cannot be undone!')}
    </p>
  </Modal>
)

DeleteTaskModal.propTypes = {
  task: PropTypes.object.isRequired,
  info: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteTaskModal
