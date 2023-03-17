import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Attribute from '../element/Attribute'
import ElementButtons from '../common/ElementButtons'

const Attributes = ({ config, attributes, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Attributes')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, attributes).map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Attributes
