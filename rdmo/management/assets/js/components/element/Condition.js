import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Condition = ({ config, condition, fetchElement, storeElement }) => {

  const verboseName = gettext('condition')

  const fetchEdit = () => fetchElement('conditions', condition.id)
  const toggleLocked = () => storeElement('conditions', {...condition, locked: !condition.locked })

  return (
    <li className="list-group-item">
      <div className="element">
        <div className="element-options">
          <EditLink element={condition} verboseName={verboseName} onClick={fetchEdit} />
          <LockedLink element={condition} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={condition} verboseName={verboseName} />
        </div>
        <div>
          <strong>{gettext('Condition')}{': '}</strong>
          <code className="code-conditions">{condition.uri}</code>
        </div>
      </div>
    </li>
  )
}

Condition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Condition
