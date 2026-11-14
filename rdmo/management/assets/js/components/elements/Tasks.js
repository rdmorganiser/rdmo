import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig, useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix} from '../common/Filter'
import Task from '../element/Task'

const Tasks = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const tasks = useSelector((state) => state.elements.tasks)

  const [filterString, setFilterString] = useConfig('filter.tasks.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.tasks.uri_prefix', '')
  const [filterSite, setFilterSite] = useConfig('filter.sites', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const [displayUriTasks, toggleDisplayUriTasks] = useConfigToggle('display.uri.tasks', true)
  const [displayUriConditions, toggleDisplayUriConditions] = useConfigToggle('display.uri.conditions', true)


  const createTask = () => dispatch(createElement('tasks'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Tasks')}</strong>
          <BackButton />
          <NewButton onClick={createTask} />
        </div>
      </div>

      <div className="card-body">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter tasks')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(tasks)} />
            </div>
            {
              settings.multisite && (
                <>
                  <div className="col-sm-2">
                    <FilterSite
                      value={filterSite} onChange={setFilterSite}
                      options={sites} />
                  </div>
                  <div className="col-sm-2">
                    <FilterSite
                      value={filterEditor} onChange={setFilterEditor}
                      options={sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                  </div>
                </>
              )
            }
          </div>
        </div>
        <div className="input-group input-group-sm row-gap-1">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriTasks} className={btnClass(displayUriTasks)}>
            {gettext('Tasks')}
          </button>
          <button type="button" onClick={toggleDisplayUriConditions} className={btnClass(displayUriConditions)}>
            {gettext('Conditions')}
          </button>
        </div>
      </div>

      {
        !isEmpty(tasks) && (
          <ul className="list-group list-group-flush border-top">
            {
              tasks.map((task, index) => (
                <Task
                  key={index} task={task}
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
