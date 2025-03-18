import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Condition from '../element/Condition'

const Conditions = ({ config, conditions, configActions, elementActions}) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.conditions.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.conditions.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.conditions.search', '')} onChange={updateFilterString}
                          label={gettext('Filter conditions')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.conditions.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(conditions)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
      </div>

      <ul className="list-group">
      {
        conditions.map((condition, index) => (
          <Condition key={index} config={config} condition={condition}
                     configActions={configActions} elementActions={elementActions}
                     filter="conditions" filterEditors={true} />
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
