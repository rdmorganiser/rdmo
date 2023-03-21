import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteTaskModal = ({ task, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete catalog')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the task:')}
    </p>
    <p>
      <code className="code-tasks">{task.uri}</code>
    </p>
    <p dangerouslySetInnerHTML={{
      __html: interpolate(ngettext(
        'This task is used in <b>one project</b>, from which it will be removed.',
        'This task is used in <b>%s projects</b>, from which it will be removed.',
        task.projects_count
      ), [task.projects_count])}} />
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteTaskModal.propTypes = {
  task: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteTaskModal
