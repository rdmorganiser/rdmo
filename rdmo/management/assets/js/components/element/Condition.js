import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/Links'

const Condition = ({ config, condition, elementActions, filter=null }) => {

  const verboseName = gettext('condition')
  const showElement = filterElement(filter, condition)

  const fetchEdit = () => elementActions.fetchElement('conditions', condition.id)
  const toggleLocked = () => elementActions.storeElement('conditions', {...condition, locked: !condition.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
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
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.object
}

export default Condition
