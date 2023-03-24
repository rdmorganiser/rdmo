import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Task = ({ config, task, elementActions, filter=null }) => {

  const verboseName = gettext('task')
  const showElement = filterElement(filter, task)

  const fetchEdit = () => elementActions.fetchElement('tasks', task.id)
  const toggleAvailable = () => elementActions.storeElement('tasks', {...task, available: !task.available })
  const toggleLocked = () => elementActions.storeElement('tasks', {...task, locked: !task.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
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
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.object
}

export default Task
