import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Condition from '../element/Condition'
import ElementButtons from '../common/ElementButtons'

const Conditions = ({ config, conditions, fetchElement, createElement, storeElement }) => {

  const createCondition = () => createElement('conditions')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onCreate={createCondition} />
        <strong>{gettext('Conditions')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, conditions).map((condition, index) => (
          <Condition key={index} config={config} condition={condition}
                     fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Conditions.propTypes = {
  config: PropTypes.object.isRequired,
  conditions: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  createElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Conditions
