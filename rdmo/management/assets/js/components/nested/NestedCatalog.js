import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Catalog from '../element/Catalog'
import Section from '../element/Section'
import ElementButtons from '../common/ElementButtons'

const NestedCatalog = ({ config, catalog, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <Catalog config={config} catalog={catalog}
                 fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, catalog.elements).map((section, index) => (
          <Section key={index} config={config} section={section}
                   fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedCatalog
