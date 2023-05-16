import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Condition from '../element/Condition'

const Conditions = ({ config, conditions, configActions, elementActions}) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.conditions.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.conditions.uri_prefix', value)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterString value={config.filter.conditions.search} onChange={updateFilterString}
                          placeholder={gettext('Filter conditions')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.conditions.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(conditions)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        conditions.map((condition, index) => (
          <Condition key={index} config={config} condition={condition} elementActions={elementActions}
                     filter={config.filter.conditions} />
        ))
      }
      </ul>
    </div>
  )
}

Conditions.propTypes = {
  config: PropTypes.object.isRequired,
  conditions: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Conditions
