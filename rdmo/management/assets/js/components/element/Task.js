import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { siteId } from 'rdmo/core/assets/js/utils/meta'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AvailableLink, LockedLink, ExportLink, CodeLink, ToggleCurrentSiteLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Task = ({ config, task, elementActions, filter=false, filterSites=false, filterEditors=false }) => {

  const showElement = filterElement(config, filter, filterSites, filterEditors, task)

  const editUrl = buildPath('tasks', task.id)
  const copyUrl = buildPath('tasks', task.id, 'copy')
  const exportUrl = buildApiPath('tasks', 'tasks', task.id, 'export')

  const getConditionUrl = (index) => buildPath('conditions', task.conditions[index])

  const fetchEdit = () => elementActions.fetchElement('tasks', task.id)
  const fetchCopy = () => elementActions.fetchElement('tasks', task.id, 'copy')
  const toggleAvailable = () => elementActions.storeElement('tasks', {...task, available: !task.available })
  const toggleLocked = () => elementActions.storeElement('tasks', {...task, locked: !task.locked })
  const toggleCurrentSite = () => elementActions.storeElement('tasks', task, 'toggle-site')

  const fetchCondition = (index) => elementActions.fetchElement('conditions', task.conditions[index])

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This task is read only')} show={task.read_only} />
          <EditLink title={gettext('Edit task')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy task')} href={copyUrl} onClick={fetchCopy} />
          <AvailableLink title={task.available ? gettext('Make task unavailable')
                                               : gettext('Make task available')}
                         available={task.available} locked={task.locked} onClick={toggleAvailable}
                         disabled={task.read_only} />
          <ToggleCurrentSiteLink hasCurrentSite={config.settings.multisite ? task.sites.includes(siteId) : true}
                         onClick={toggleCurrentSite}
                         show={config.settings.multisite}/>
          <LockedLink title={task.locked ? gettext('Unlock task') : gettext('Lock task')}
                      locked={task.locked} onClick={toggleLocked} disabled={task.read_only} />
          <ExportLink title={gettext('Export task')} exportUrl={exportUrl}
                      exportFormats={config.settings.export_formats} full={true} />
        </div>
        <div>
          <p>
            <strong>{gettext('Task')}{': '}</strong>
            <span dangerouslySetInnerHTML={{ __html: task.title }}></span>
          </p>
          {
            get(config, 'display.uri.tasks', true) && <p>
              <CodeLink className="code-tasks" uri={task.uri} href={editUrl} onClick={() => fetchEdit()} />
            </p>
          }
          {
            get(config, 'display.uri.conditions', true) && task.condition_uris.map((uri, index) => (
              <p key={index}>
                <CodeLink
                  className="code-conditions"
                  uri={uri}
                  href={getConditionUrl(index)}
                  onClick={() => fetchCondition(index)}
                />
              </p>
            ))
          }
          <ElementErrors element={task} />
        </div>
      </div>
    </li>
  )
}

Task.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default Task
