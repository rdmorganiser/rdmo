import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/Links'

const Option = ({ config, option, elementActions, display='list', indent=0, filter=null }) => {

  const verboseName = gettext('option')
  const showElement = filterElement(filter, option)

  const fetchEdit = () => elementActions.fetchElement('options', option.id)
  const toggleLocked = () => elementActions.storeElement('options', {...option, locked: !option.locked })

  const elementNode = (
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
        {
          config.display.uri.options && <p>
            <code className="code-options">{option.uri}</code>
          </p>
        }
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'nested':
      return showElement && (
        <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
          <div className="panel-body">
            { elementNode }
          </div>
        </div>
      )
  }
}

Option.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.object
}

export default Option
