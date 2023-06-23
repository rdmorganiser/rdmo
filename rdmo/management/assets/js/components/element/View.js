import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AvailableLink, LockedLink, ExportLink, CodeLink } from '../common/Links'

const View = ({ config, view, elementActions, filter=null }) => {

  const showElement = filterElement(filter, view)

  const editUrl = buildPath(config.baseUrl, 'views', view.id)
  const copyUrl = buildPath(config.baseUrl, 'views', view.id, 'copy')
  const exportUrl = buildPath('/api/v1/', 'views', 'views', view.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('views', view.id)
  const fetchCopy = () => elementActions.fetchElement('views', view.id, 'copy')
  const toggleAvailable = () => elementActions.storeElement('views', {...view, available: !view.available })
  const toggleLocked = () => elementActions.storeElement('views', {...view, locked: !view.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <EditLink title={gettext('Edit view')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy view')} href={copyUrl} onClick={fetchCopy} />
          <AvailableLink title={view.available ? gettext('Make view unavailable')
                                               : gettext('Make view available')}
                         available={view.available} locked={view.locked} onClick={toggleAvailable} />
          <LockedLink title={view.locked ? gettext('Unlock view') : gettext('Lock view')}
                      locked={view.locked} onClick={toggleLocked} />
          <ExportLink title={gettext('Export view')} exportUrl={exportUrl}
                      exportFormats={config.settings.export_formats} />
        </div>
        <div>
          <p>
            <strong>{gettext('View')}{': '}</strong>
            <CodeLink className="code-views" uri={view.uri} onClick={() => fetchEdit()} />
          </p>
          <ElementErrors element={view} />
        </div>
      </div>
    </li>
  )
}

View.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.object
}

export default View
