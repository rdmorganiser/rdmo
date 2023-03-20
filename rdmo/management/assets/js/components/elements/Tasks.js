import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Task from '../element/Task'
import { BackButton, NewButton } from '../common/ElementButtons'

const Tasks = ({ config, tasks, elementActions }) => {

  const createTask = () => elementActions.createElement('tasks')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createTask} />
        </div>
        <strong>{gettext('Tasks')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, tasks).map((task, index) => (
          <Task key={index} config={config} task={task}
                elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Tasks.propTypes = {
  config: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Tasks
