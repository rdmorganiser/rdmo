import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Option = ({ config, option, elementActions }) => {

  const verboseName = gettext('option')

  const fetchEdit = () => elementActions.fetchElement('options', option.id)
  const toggleLocked = () => elementActions.storeElement('options', {...option, locked: !option.locked })

  return (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <EditLink element={option} verboseName={verboseName} onClick={fetchEdit} />
          <LockedLink element={option} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={option} verboseName={verboseName} />
        </div>
        <div>
          <p>
            <strong>{gettext('Option')}{': '}</strong> {option.text}
          </p>
          <p>
            <code className="code-options">{option.uri}</code>
          </p>
        </div>
      </div>
    </li>
  )
}

Option.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Option
