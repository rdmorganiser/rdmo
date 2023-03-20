import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Attribute = ({ config, attribute, elementActions, list=true, indent=0 }) => {

  const verboseName = gettext('attribute')

  const fetchEdit = () => elementActions.fetchElement('attributes', attribute.id)
  const fetchNested = () => elementActions.fetchElement('attributes', attribute.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('attributes', {...attribute, locked: !attribute.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={attribute} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={attribute} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={attribute} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={attribute} verboseName={verboseName} />
      </div>
      <div style={{ paddingLeft: 15 * indent }}>
        <strong>{gettext('Attribute')}{': '}</strong>
        <code className="code-domain">{attribute.uri}</code>
      </div>
    </div>
  )

  if (list) {
    return (
      <React.Fragment>
        <li className="list-group-item">
          { elementNode }
        </li>
        {
          filterElements(config, attribute.elements).map((attribute, index) => (
            <Attribute key={index} config={config} attribute={attribute}
                       elementActions={elementActions} indent={indent + 1}/>
          ))
        }
      </React.Fragment>
    )
  } else {
    return elementNode
  }
}

Attribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  list: PropTypes.bool,
  indent: PropTypes.number
}

export default Attribute
