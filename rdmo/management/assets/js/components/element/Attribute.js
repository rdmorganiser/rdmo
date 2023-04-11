import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElement } from '../../utils/filter'

import { ElementErrors } from '../common/Errors'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink, CodeLink } from '../common/Links'

const Attribute = ({ config, attribute, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('attribute')
  const showElement = filterElement(filter, attribute)

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
      <div>
        <p>
          <strong>{gettext('Attribute')}{': '}</strong>
          <CodeLink className="code-domain" uri={attribute.uri} onClick={() => fetchEdit()} />
        </p>
        <ElementErrors element={attribute} />
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
      return (
        <>
          {
            showElement && <div className="panel panel-default" style={{ marginLeft: 30 * indent }}>
              <div className="panel-body">
                { elementNode }
              </div>
            </div>
          }
          {
            attribute.elements.map((attribute, index) => (
              <Attribute key={index} config={config} attribute={attribute} elementActions={elementActions}
                         display="nested" filter={filter} indent={indent + 1} />
            ))
          }
        </>
      )
    case 'plain':
      return elementNode
  }
}

Attribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default Attribute
