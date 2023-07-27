import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import OptionSet from '../element/OptionSet'

const OptionSets = ({ config, optionsets, configActions, elementActions}) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.optionsets.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.optionsets.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.optionsets.editors', value)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterString value={config.filter.optionsets.search} onChange={updateFilterString}
                          placeholder={gettext('Filter option sets')} />
          </div>
          <div className={config.settings.multisite ? 'col-sm-2' : 'col-sm-4'}>
            <FilterUriPrefix value={config.filter.optionsets.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(optionsets)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={config.filter.optionsets.editors} onChange={updateFilterEditor}
                          options={config.sites} allLabel='All editors' />
            </div>
          }
        </div>
      </div>

      <ul className="list-group">
      {
        optionsets.map((optionset, index) => (
          <OptionSet key={index} config={config} optionset={optionset} elementActions={elementActions}
                     filter={config.filter.optionsets} />
        ))
      }
      </ul>
    </div>
  )
}

OptionSets.propTypes = {
  config: PropTypes.object.isRequired,
  optionsets: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default OptionSets
