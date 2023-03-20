import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Option from '../element/Option'
import { BackButton, NewButton } from '../common/ElementButtons'

const Options = ({ config, options, elementActions }) => {

  const createOption = () => elementActions.createElement('options')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createOption} />
        </div>
        <strong>{gettext('Options')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, options).map((option, index) => (
          <Option key={index} config={config} option={option}
                  elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Options.propTypes = {
  config: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Options
