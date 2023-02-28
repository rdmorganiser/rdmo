import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Tasks = ({ config, tasks, fetchTask }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit task')}
                   onClick={event => handleEdit(event, task.id)}>
                </a>
                {' '}
                <a href={task.xml_url} className="fa fa-download"
                   title={gettext('Export task as XML')}
                   target="blank">
                </a>
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
  fetchTask: PropTypes.func.isRequired
}

export default Tasks
