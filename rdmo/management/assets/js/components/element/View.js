import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const View = ({ config, view, fetchElement, storeElement }) => {

  const verboseName = gettext('view')

  const fetchEdit = () => fetchElement('views', view.id)
  const toggleAvailable = () => storeElement('views', {...view, available: !view.available })
  const toggleLocked = () => storeElement('views', {...view, locked: !view.locked })

  return (
    <li className="list-group-item">
      <div className="element">
        <div className="element-options">
          <EditLink element={view} verboseName={verboseName} onClick={fetchEdit} />
          <AvailableLink element={view} verboseName={verboseName} onClick={toggleAvailable} />
          <LockedLink element={view} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={view} verboseName={verboseName} />
        </div>
        <div>
          <strong>{gettext('View')}{': '}</strong>
          <code className="code-views">{view.uri}</code>
        </div>
      </div>
    </li>
  )
}

View.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default View
