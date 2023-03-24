import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Option from '../element/Option'
import { BackButton, NewButton } from '../common/ElementButtons'

const Options = ({ config, options, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.options.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.options.uriPrefix', uriPrefix)

  const createOption = () => elementActions.createElement('options')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createOption} />
        </div>
        <strong>{gettext('Options')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.options.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter options by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.options.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(options)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        options.map((option, index) => (
          <Option key={index} config={config} option={option} elementActions={elementActions}
                  filter={config.filter.options} />
        ))
      }
      </ul>
    </div>
  )
}

Options.propTypes = {
  config: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Options
