import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Attribute from '../element/Attribute'
import { BackButton, NewButton } from '../common/ElementButtons'

const Attributes = ({ config, attributes, elementActions }) => {

  const createAttribute = () => elementActions.createElement('attributes')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createAttribute} />
        </div>
        <strong>{gettext('Attributes')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, attributes).map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Attributes
