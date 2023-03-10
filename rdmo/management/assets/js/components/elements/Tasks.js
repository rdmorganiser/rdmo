import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Tasks = ({ config, tasks, fetchTask, storeTask }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchTask(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Tasks')} />

      <ul className="list-group">
      {
        filterElements(config, tasks).map((task, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={task} verboseName={gettext('task')}
                          onClick={task => fetchTask(task.id)} />
                <AvailableLink element={task} verboseName={gettext('task')}
                               onClick={available => storeTask(Object.assign({}, task, { available }))} />
                <LockedLink element={task} verboseName={gettext('task')}
                            onClick={locked => storeTask(Object.assign({}, task, { locked }))} />
                <ExportLink element={task} verboseName={gettext('task')} />
              </div>
              <div>
                <strong>{gettext('Task')}{': '}</strong>
                <code className="code-tasks">{task.uri}</code>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Tasks.propTypes = {
  config: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired,
  fetchTask: PropTypes.func.isRequired,
  storeTask: PropTypes.func.isRequired
}

export default Tasks
