import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'
import { Checkbox } from '../common/Checkboxes'

import Task from '../element/Task'

const Tasks = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const tasks = useSelector((state) => state.elements.tasks)

  const updateFilterString = (value) => dispatch(updateConfig('filter.tasks.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.tasks.uri_prefix', value))
  const updateFilterSite = (value) => dispatch(updateConfig('filter.sites', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const updateDisplayTasksURI = (value) => dispatch(updateConfig('display.uri.tasks', value))
  const updateDisplayConditionsURI = (value) => dispatch(updateConfig('display.uri.conditions', value))

  const createTask = () => dispatch(createElement('tasks'))

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
            <FilterString value={get(config, 'filter.tasks.search', '')} onChange={updateFilterString}
                          label={gettext('Filter tasks')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.tasks.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(tasks)} />
          </div>
          {
            config.settings.multisite && <>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.sites', '')} onChange={updateFilterSite}
                            options={config.sites} />
              </div>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                            options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            </>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-tasks">{gettext('Tasks')}</code>}
                    value={get(config, 'display.uri.tasks', true)} onChange={updateDisplayTasksURI} />
          <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                    value={get(config, 'display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
        </div>

      </div>

      <ul className="list-group">
      {
        tasks.map((task, index) => (
          <Task key={index} config={config} task={task}
                filter="tasks" filterSites={true} filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default Tasks
