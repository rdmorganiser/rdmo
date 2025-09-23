import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Condition from '../element/Condition'

const Conditions = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const conditions = useSelector((state) => state.elements.conditions)

  const updateFilterString = (value) => dispatch(updateConfig('filter.conditions.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.conditions.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const createCondition = () => dispatch(createElement('conditions'))

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
                     filter="conditions" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default Conditions
