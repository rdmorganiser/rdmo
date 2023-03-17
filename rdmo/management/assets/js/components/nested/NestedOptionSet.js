import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Option from '../element/Option'
import OptionSet from '../element/OptionSet'
import ElementButtons from '../common/ElementButtons'


const NestedOptionSet = ({ config, optionset, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <OptionSet config={config} optionset={optionset}
                   fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, optionset.elements).map((option, index) => (
          <Option key={index} config={config} option={option}
                  fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

NestedOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedOptionSet
