import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Task from '../element/Task'
import ElementButtons from '../common/ElementButtons'

const Tasks = ({ config, tasks, fetchElement, createElement, storeElement }) => {

  const createTask = () => createElement('tasks')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onCreate={createTask} />
        <strong>{gettext('Tasks')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, tasks).map((task, index) => (
          <Task key={index} config={config} task={task}
                fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Tasks.propTypes = {
  config: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  createElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Tasks
