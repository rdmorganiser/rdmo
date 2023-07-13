import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite, FilterEditor } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Task from '../element/Task'

const Tasks = ({ config, tasks, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.tasks.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.tasks.uri_prefix', value)
  const updateFilterSite = (value) => configActions.updateConfig('filter.tasks.sites', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.tasks.editors', value)

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
          <div className={config.settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
            <FilterString value={config.filter.tasks.search} onChange={updateFilterString}
                          placeholder={gettext('Filter tasks')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.tasks.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(tasks)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={config.filter.tasks.sites} onChange={updateFilterSite}
                          options={config.sites} />
            </div>
          }
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterEditor value={config.filter.tasks.editors} onChange={updateFilterEditor}
                          options={config.sites} />
            </div>
          }
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
