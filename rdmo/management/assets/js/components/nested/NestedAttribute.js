import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Attribute from '../element/Attribute'
import ElementButtons from '../common/ElementButtons'

const NestedAttribute = ({ config, attribute, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <Attribute config={config} attribute={attribute}
                   fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, attribute.elements).map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     fetchElement={fetchElement} storeElement={storeElement} indent={1} />
        ))
      }
      </ul>
    </div>
  )
}

NestedAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedAttribute
