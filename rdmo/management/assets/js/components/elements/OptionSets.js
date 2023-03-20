import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import OptionSet from '../element/OptionSet'
import { BackButton, NewButton } from '../common/ElementButtons'

const OptionSets = ({ config, optionsets , elementActions}) => {

  const createOptionSet = () => elementActions.createElement('optionsets')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createOptionSet} />
        </div>
        <strong>{gettext('Option sets')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, optionsets).map((optionset, index) => (
          <OptionSet key={index} config={config} optionset={optionset}
                     elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

OptionSets.propTypes = {
  config: PropTypes.object.isRequired,
  optionsets: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default OptionSets
