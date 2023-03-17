import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Option from '../element/Option'
import ElementButtons from '../common/ElementButtons'

const Options = ({ config, options, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Options')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, options).map((option, index) => (
          <Option key={index} config={config} option={option}
                  fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Options.propTypes = {
  config: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Options
