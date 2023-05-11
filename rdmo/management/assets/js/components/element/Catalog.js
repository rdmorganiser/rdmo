import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElement } from '../../utils/filter'

import Section from './Section'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, AvailableLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'

const Catalog = ({ config, catalog, elementActions, display='list', filter=null }) => {

  const verboseName = gettext('catalog')
  const showElement = filterElement(filter, catalog)

  const fetchEdit = () => elementActions.fetchElement('catalogs', catalog.id)
  const fetchCopy = () => elementActions.fetchElement('catalogs', catalog.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('catalogs', catalog.id, 'nested')
  const toggleAvailable = () => elementActions.storeElement('catalogs', {...catalog, available: !catalog.available })
  const toggleLocked = () => elementActions.storeElement('catalogs', {...catalog, locked: !catalog.locked })

  const createSection = () => elementActions.createElement('sections', { catalog })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={catalog} verboseName={verboseName} onClick={fetchEdit} />
        <CopyLink element={catalog} verboseName={verboseName} onClick={fetchCopy} />
        <AddLink element={catalog} verboseName={gettext('section')} onClick={createSection} />
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
          config.display.uri.catalogs &&
          <CodeLink className="code-questions" uri={catalog.uri} onClick={() => fetchEdit()} />
        }
        <ElementErrors element={catalog} />
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
