import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Option from '../element/Option'
import OptionSet from '../element/OptionSet'
import { BackButton } from '../common/ElementButtons'

const NestedOptionSet = ({ config, optionset, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.optionset.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.optionset.uriPrefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <OptionSet config={config} optionset={optionset}
                     elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.optionset.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter optionsets by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.optionset.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(optionset.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        optionset.elements.map((option, index) => (
          <Option key={index} config={config} option={option} elementActions={elementActions}
                  display="nested" filter={config.filter.optionset} indent={1} />
        ))
      }
    </>
  )
}

NestedOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedOptionSet
