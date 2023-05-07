import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, LockedLink, ExportLink, CodeLink } from '../common/Links'

const Condition = ({ config, condition, elementActions, filter=null }) => {

  const verboseName = gettext('condition')
  const showElement = filterElement(filter, condition)

  const fetchEdit = () => elementActions.fetchElement('conditions', condition.id)
  const fetchCopy = () => elementActions.fetchElement('conditions', condition.id, 'copy')
  const toggleLocked = () => elementActions.storeElement('conditions', {...condition, locked: !condition.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <EditLink element={condition} verboseName={verboseName} onClick={fetchEdit} />
          <CopyLink element={condition} verboseName={verboseName} onClick={fetchCopy} />
          <LockedLink element={condition} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={condition} verboseName={verboseName} />
        </div>
        <div>
          <p>
            <strong>{gettext('Condition')}{': '}</strong>
            <CodeLink className="code-conditions" uri={condition.uri} onClick={() => fetchEdit()} />
          </p>
          <ElementErrors element={condition} />
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
