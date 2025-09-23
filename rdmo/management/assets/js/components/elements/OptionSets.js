import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import OptionSet from '../element/OptionSet'

const OptionSets = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const optionsets = useSelector((state) => state.elements.optionsets)

  const updateFilterString = (value) => dispatch(updateConfig('filter.optionsets.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.optionsets.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const createOptionSet = () => dispatch(createElement('optionsets'))

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createOptionSet} />
        </div>
        <strong>{gettext('Option sets')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.optionsets.search', '')} onChange={updateFilterString}
                          label={gettext('Filter option sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.optionsets.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(optionsets)} />
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
        optionsets.map((optionset, index) => (
          <OptionSet key={index} config={config} optionset={optionset}
                     filter="optionsets" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default OptionSets
