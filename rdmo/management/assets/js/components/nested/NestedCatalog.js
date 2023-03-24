import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Catalog from '../element/Catalog'
import Section from '../element/Section'
import { BackButton } from '../common/ElementButtons'

const NestedCatalog = ({ config, catalog, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.catalog.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.catalog.uriPrefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Catalog config={config} catalog={catalog}
                   elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.catalog.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter catalogs by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.catalog.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(catalog.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        catalog.elements.map((section, index) => (
          <Section key={index} config={config} section={section} elementActions={elementActions}
                   display="nested" filter={config.filter.catalog} indent={0} />
        ))
      }
    </>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedCatalog
