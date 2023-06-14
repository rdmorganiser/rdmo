import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AvailableLink, LockedLink, ExportLink, CodeLink } from '../common/Links'

const View = ({ config, view, elementActions, filter=null }) => {

  const verboseName = gettext('view')
  const showElement = filterElement(filter, view)

  const fetchEdit = () => elementActions.fetchElement('views', view.id)
  const fetchCopy = () => elementActions.fetchElement('views', view.id, 'copy')
  const toggleAvailable = () => elementActions.storeElement('views', {...view, available: !view.available })
  const toggleLocked = () => elementActions.storeElement('views', {...view, locked: !view.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <EditLink verboseName={verboseName} onClick={fetchEdit} />
          <CopyLink verboseName={verboseName} onClick={fetchCopy} />
          <AvailableLink element={view} verboseName={verboseName} onClick={toggleAvailable} />
          <LockedLink element={view} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={view} elementType="views" verboseName={verboseName}
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
