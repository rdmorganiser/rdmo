import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
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
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Option sets')}</strong>
          <BackButton />
          <NewButton onClick={createOptionSet} />
        </div>
      </div>

      <div className="card-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString
              value={get(config, 'filter.optionsets.search', '')} onChange={updateFilterString}
              label={gettext('Filter option sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix
              value={get(config, 'filter.optionsets.uri_prefix', '')} onChange={updateFilterUriPrefix}
              options={getUriPrefixes(optionsets)} />
          </div>
          {
            config.settings.multisite && (
              <div className="col-sm-2">
                <FilterSite
                  value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                  options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            )
          }
        </div>
      </div>

      {
        !isEmpty(optionsets) && (
          <ul className="list-group list-group-flush">
            {
              optionsets.map((optionset, index) => (
                <OptionSet
                  key={index} config={config} optionset={optionset}
                  filter="optionsets" filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default OptionSets
