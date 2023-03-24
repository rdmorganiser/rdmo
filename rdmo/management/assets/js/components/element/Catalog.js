import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElement } from '../../utils/filter'

import Section from './Section'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/Links'

const Catalog = ({ config, catalog, elementActions, display='list', filter=null }) => {

  const verboseName = gettext('catalog')
  const showElement = filterElement(filter, catalog)

  const fetchEdit = () => elementActions.fetchElement('catalogs', catalog.id)
  const fetchNested = () => elementActions.fetchElement('catalogs', catalog.id, 'nested')
  const toggleAvailable = () => elementActions.storeElement('catalogs', {...catalog, available: !catalog.available })
  const toggleLocked = () => elementActions.storeElement('catalogs', {...catalog, locked: !catalog.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={catalog} verboseName={verboseName} onClick={fetchEdit} />
        <AvailableLink element={catalog} verboseName={verboseName} onClick={toggleAvailable} />
        <LockedLink element={catalog} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={catalog} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={catalog} verboseName={verboseName} />
      </div>
      <div>
        <p>
          <strong>{gettext('Catalog')}{': '}</strong> {catalog.title}
        </p>
        {
          config.display.uri.catalogs && <p>
            <code className="code-questions">{catalog.uri}</code>
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
    case 'plain':
      return elementNode
  }
}

Catalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object
}

export default Catalog
