import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Task = ({ config, task, fetchElement, storeElement }) => {

  const verboseName = gettext('task')

  const fetchEdit = () => fetchElement('tasks', task.id)
  const toggleAvailable = () => storeElement('tasks', {...task, available: !task.available })
  const toggleLocked = () => storeElement('tasks', {...task, locked: !task.locked })

  return (
    <li className="list-group-item">
      <div className="element">
        <div className="element-options">
          <EditLink element={task} verboseName={verboseName} onClick={fetchEdit} />
          <AvailableLink element={task} verboseName={verboseName} onClick={toggleAvailable} />
          <LockedLink element={task} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={task} verboseName={verboseName} />
        </div>
        <div>
          <strong>{gettext('Task')}{': '}</strong>
          <code className="code-tasks">{task.uri}</code>
        </div>
      </div>
    </li>
  )
}

Task.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Task
