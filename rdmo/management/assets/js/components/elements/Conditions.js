import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Condition from '../element/Condition'
import { BackButton, NewButton } from '../common/ElementButtons'

const Conditions = ({ config, conditions , elementActions}) => {

  const createCondition = () => elementActions.createElement('conditions')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createCondition} />
        </div>
        <strong>{gettext('Conditions')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, conditions).map((condition, index) => (
          <Condition key={index} config={config} condition={condition}
                     elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Conditions.propTypes = {
  config: PropTypes.object.isRequired,
  conditions: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Conditions
