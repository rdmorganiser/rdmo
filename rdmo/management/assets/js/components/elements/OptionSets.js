import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import OptionSet from '../element/OptionSet'
import ElementButtons from '../common/ElementButtons'

const OptionSets = ({ config, optionsets, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Option sets')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, optionsets).map((optionset, index) => (
          <OptionSet key={index} config={config} optionset={optionset}
                     fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

OptionSets.propTypes = {
  config: PropTypes.object.isRequired,
  optionsets: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default OptionSets
