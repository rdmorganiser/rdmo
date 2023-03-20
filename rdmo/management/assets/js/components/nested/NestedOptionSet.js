import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Option from '../element/Option'
import OptionSet from '../element/OptionSet'
import { BackButton } from '../common/ElementButtons'

const NestedOptionSet = ({ config, optionset, elementActions }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
        </div>
        <OptionSet config={config} optionset={optionset}
                   elementActions={elementActions} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, optionset.elements).map((option, index) => (
          <Option key={index} config={config} option={option}
                  elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

NestedOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedOptionSet
