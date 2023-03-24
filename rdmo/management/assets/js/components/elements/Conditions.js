import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Condition from '../element/Condition'
import { BackButton, NewButton } from '../common/ElementButtons'

const Conditions = ({ config, conditions, configActions, elementActions}) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.conditions.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.conditions.uriPrefix', uriPrefix)

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
            <FilterUri value={config.filter.conditions.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter conditions by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.conditions.uriPrefix} onChange={updateFilterUriPrefix}
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
