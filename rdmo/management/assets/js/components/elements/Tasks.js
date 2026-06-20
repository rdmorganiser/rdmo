import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix} from '../common/Filter'
import Task from '../element/Task'

const Tasks = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const tasks = useSelector((state) => state.elements.tasks)

  const updateFilterString = (value) => dispatch(updateConfig('filter.tasks.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.tasks.uri_prefix', value))
  const updateFilterSite = (value) => dispatch(updateConfig('filter.sites', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriTasks = isTruthy(get(config, 'display.uri.tasks', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const updateDisplayUriTasks = () => dispatch(updateConfig('display.uri.tasks', !displayUriTasks))
  const updateDisplayUriConditions = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))

  const createTask = () => dispatch(createElement('tasks'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Tasks')}</strong>
          <BackButton />
          <NewButton onClick={createTask} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
            <FilterString
              value={get(config, 'filter.tasks.search', '')} onChange={updateFilterString}
              label={gettext('Filter tasks')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix
              value={get(config, 'filter.tasks.uri_prefix', '')} onChange={updateFilterUriPrefix}
              options={getUriPrefixes(tasks)} />
          </div>
          {
            config.settings.multisite && (
              <>
                <div className="col-sm-2">
                  <FilterSite
                    value={get(config, 'filter.sites', '')} onChange={updateFilterSite}
                    options={config.sites} />
                </div>
                <div className="col-sm-2">
                  <FilterSite
                    value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                    options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                </div>
              </>
            )
          }
        </div>
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={updateDisplayUriTasks} className={btnClass(displayUriTasks)}>
            {gettext('Tasks')}
          </button>
          <button type="button" onClick={updateDisplayUriConditions} className={btnClass(displayUriConditions)}>
            {gettext('Conditions')}
          </button>
        </div>
      </div>

      {
        !isEmpty(tasks) && (
          <ul className="list-group list-group-flush">
            {
              tasks.map((task, index) => (
                <Task
                  key={index} config={config} task={task}
                  filter="tasks" filterSites={true} filterEditors={true} />
              ))
            }
          </ul>

        )
      }
    </div>
  )
}

export default Tasks
