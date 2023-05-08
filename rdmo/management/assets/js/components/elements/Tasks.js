import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Task from '../element/Task'

const Tasks = ({ config, tasks, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.tasks.string', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.tasks.uriPrefix', value)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterString value={config.filter.tasks.string} onChange={updateFilterString}
                          placeholder={gettext('Filter tasks')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.tasks.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(tasks)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        tasks.map((task, index) => (
          <Task key={index} config={config} task={task} elementActions={elementActions}
                filter={config.filter.tasks} />
        ))
      }
      </ul>
    </div>
  )
}

Tasks.propTypes = {
  config: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Tasks
