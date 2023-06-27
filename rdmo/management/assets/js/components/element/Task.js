import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AvailableLink, LockedLink, ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Task = ({ config, task, elementActions, filter=null }) => {

  const showElement = filterElement(filter, task)

  const editUrl = buildPath(config.baseUrl, 'tasks', task.id)
  const copyUrl = buildPath(config.baseUrl, 'tasks', task.id, 'copy')
  const exportUrl = buildPath('/api/v1/', 'tasks', 'tasks', task.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('tasks', task.id)
  const fetchCopy = () => elementActions.fetchElement('tasks', task.id, 'copy')
  const toggleAvailable = () => elementActions.storeElement('tasks', {...task, available: !task.available })
  const toggleLocked = () => elementActions.storeElement('tasks', {...task, locked: !task.locked })

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
          <LockedLink title={task.locked ? gettext('Unlock task') : gettext('Lock task')}
                      locked={task.locked} onClick={toggleLocked} disabled={task.read_only} />
          <ExportLink title={gettext('Export task')} exportUrl={exportUrl}
                      exportFormats={config.settings.export_formats} full={true} />
        </div>
        <div>
          <p>
            <strong>{gettext('Task')}{': '}</strong>
            <CodeLink className="code-tasks" uri={task.uri} onClick={() => fetchEdit()} />
          </p>
          <ElementErrors element={task} />
        </div>
      </div>
    </li>
  )
}

Task.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.object
}

export default Task
