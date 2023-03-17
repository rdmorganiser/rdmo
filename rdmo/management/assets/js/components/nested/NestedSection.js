import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Section from '../element/Section'
import Page from '../element/Page'
import ElementButtons from '../common/ElementButtons'

const NestedCatalog = ({ config, section, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <Section config={config} section={section}
                 fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, section.elements).map((page, index) => (
          <Page key={index} config={config} page={page}
                fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedCatalog
