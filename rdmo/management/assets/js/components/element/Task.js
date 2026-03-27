import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'
import { siteId } from 'rdmo/core/assets/js/utils/meta'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import {
  AvailableLink,
  CodeLink,
  CopyLink,
  EditLink,
  ExportLink,
  LockedLink,
  ToggleCurrentSiteLink
} from '../common/Links'

const Task = ({ task, filter = false, filterSites = false, filterEditors = false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, filterSites, filterEditors, task)

  const editUrl = buildPath('tasks', task.id)
  const copyUrl = buildPath('tasks', task.id, 'copy')
  const exportUrl = buildApiPath('tasks', 'tasks', task.id, 'export')

  const getConditionUrl = (index) => buildPath('conditions', task.conditions[index])

  const fetchEdit = () => dispatch(fetchElement('tasks', task.id))
  const fetchCopy = () => dispatch(fetchElement('tasks', task.id, 'copy'))
  const toggleAvailable = () => dispatch(storeElement('tasks', { ...task, available: !task.available }))
  const toggleLocked = () => dispatch(storeElement('tasks', { ...task, locked: !task.locked }))
  const toggleCurrentSite = () => dispatch(storeElement('tasks', task, 'toggle-site'))

  const fetchCondition = (index) => dispatch(fetchElement('conditions', task.conditions[index]))

  const displayUriTasks = isTruthy(get(config, 'display.uri.tasks', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  return showElement && (
    <li className="list-group-item">
      <div className="d-flex flex-column gap-2">
        <div className="d-flex align-items-center gap-2">
          <strong>{gettext('Task')}{':'}</strong>
          <div className="flex-grow-1">
            <Html html={task.title} />
          </div>

          <div className="d-flex align-items-center gap-1">
            <ReadOnlyIcon title={gettext('This task is read only')} show={task.read_only} />
            <EditLink title={gettext('Edit task')} href={editUrl} onClick={fetchEdit} />
            <CopyLink title={gettext('Copy task')} href={copyUrl} onClick={fetchCopy} />
            <AvailableLink
              title={
                task.available ? gettext('Make task unavailable') : gettext('Make task available')
              }
              available={task.available} locked={task.locked} onClick={toggleAvailable}
              disabled={task.read_only} />
            <ToggleCurrentSiteLink hasCurrentSite={config.settings.multisite ? task.sites.includes(siteId) : true}
              onClick={toggleCurrentSite}
              show={config.settings.multisite} />
            <LockedLink title={task.locked ? gettext('Unlock task') : gettext('Lock task')}
              locked={task.locked} onClick={toggleLocked} disabled={task.read_only} />
            <ExportLink title={gettext('Export task')} exportUrl={exportUrl}
              exportFormats={config.settings.export_formats} full={true} />
          </div>
        </div>
        {
          displayUriTasks && (
            <CodeLink type="tasks" uri={task.uri} href={editUrl} onClick={() => fetchEdit()} />
          )
        }
        {
          displayUriConditions && task.condition_uris.map((uri, index) => (
            <CodeLink
              key={index}
              type="conditions"
              uri={uri}
              href={getConditionUrl(index)}
              onClick={() => fetchCondition(index)}
            />
          ))
        }
        <ElementErrors element={task} />
      </div>
    </li>
  )
}

Task.propTypes = {
  task: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default Task
