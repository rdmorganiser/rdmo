import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Attribute from '../element/Attribute'
import { BackButton } from '../common/ElementButtons'

const NestedAttribute = ({ config, attribute, elementActions }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
        </div>
        <Attribute config={config} attribute={attribute}
                   elementActions={elementActions} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, attribute.elements).map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     elementActions={elementActions} indent={1} />
        ))
      }
      </ul>
    </div>
  )
}

NestedAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedAttribute
