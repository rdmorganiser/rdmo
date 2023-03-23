import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import OptionSet from '../element/OptionSet'
import { BackButton, NewButton } from '../common/ElementButtons'

const OptionSets = ({ config, optionsets, configActions, elementActions}) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.optionsets.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.optionsets.uriPrefix', uriPrefix)

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
            <FilterUri value={config.filter.optionsets.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter optionsets by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.optionsets.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(optionsets)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        filterElements(config.filter.optionsets, optionsets).map((optionset, index) => (
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
