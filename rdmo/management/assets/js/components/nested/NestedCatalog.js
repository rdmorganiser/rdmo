import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Catalog from '../element/Catalog'
import Section from '../element/Section'
import { BackButton } from '../common/ElementButtons'

const NestedCatalog = ({ config, catalog, elementActions }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
        </div>
        <Catalog config={config} catalog={catalog}
                 elementActions={elementActions} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, catalog.elements).map((section, index) => (
          <Section key={index} config={config} section={section}
                   elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedCatalog
