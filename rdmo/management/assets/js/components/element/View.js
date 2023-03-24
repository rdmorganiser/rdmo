import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/Links'

const View = ({ config, view, elementActions, filter=null }) => {

  const verboseName = gettext('view')
  const showElement = filterElement(filter, view)

  const fetchEdit = () => elementActions.fetchElement('views', view.id)
  const toggleAvailable = () => elementActions.storeElement('views', {...view, available: !view.available })
  const toggleLocked = () => elementActions.storeElement('views', {...view, locked: !view.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
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
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.object
}

export default View
