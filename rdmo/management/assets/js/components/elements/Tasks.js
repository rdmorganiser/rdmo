import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Task from '../element/Task'
import { BackButton, NewButton } from '../common/ElementButtons'

const Tasks = ({ config, tasks, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.tasks.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.tasks.uriPrefix', uriPrefix)

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
            <FilterUri value={config.filter.tasks.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter tasks by URI')} />
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
