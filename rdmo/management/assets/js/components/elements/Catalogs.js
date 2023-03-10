import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Catalogs = ({ config, catalogs, fetchCatalog, storeCatalog }) => {
  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, catalogs).map((catalog, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={catalog} verboseName={gettext('catalog')}
                          onClick={catalog => fetchCatalog(catalog.id)} />
                <AvailableLink element={catalog} verboseName={gettext('catalog')}
                              onClick={available => storeCatalog(Object.assign({}, catalog, { available }))} />
                <LockedLink element={catalog} verboseName={gettext('catalog')}
                          onClick={locked => storeCatalog(Object.assign({}, catalog, { locked }))} />
                <ExportLink element={catalog} verboseName={gettext('catalog')} />
              </div>
              <div>
                <p>
                  <strong>{gettext('Catalog')}{': '}</strong> {catalog.title}
                </p>
                <p>
                  <code className="code-questions">{catalog.uri}</code>
                </p>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  fetchCatalog: PropTypes.func.isRequired,
  storeCatalog: PropTypes.func.isRequired
}

export default Catalogs
