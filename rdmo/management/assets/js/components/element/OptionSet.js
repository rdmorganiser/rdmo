import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import Option from './Option'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const OptionSet = ({ config, optionset, elementActions, list=true }) => {

  const verboseName = gettext('option set')

  const fetchEdit = () => elementActions.fetchElement('optionsets', optionset.id)
  const fetchNested = () => elementActions.fetchElement('optionsets', optionset.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('optionsets', {...optionset, locked: !optionset.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={optionset} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={optionset} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={optionset} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={optionset} verboseName={verboseName} />
      </div>
      <div>
        <strong>{gettext('Option set')}{': '}</strong>
        <code className="code-options">{optionset.uri}</code>
      </div>
    </div>
  )

  if (list) {
    return (
      <li className="list-group-item">
        { elementNode }
      </li>
    )
  } else {
    return elementNode
  }
}

OptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  list: PropTypes.bool
}

export default OptionSet
