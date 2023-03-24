import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Option from '../element/Option'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

const Options = ({ config, options, configActions, elementActions }) => {

  const updateFilterUri = (value) => configActions.updateConfig('filter.options.uri', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.options.uriPrefix', value)
  const updateDisplayURI = (value) => configActions.updateConfig('display.uri.options', value)

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
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-options">{gettext('Options')}</code>}
                    value={config.display.uri.options} onChange={updateDisplayURI} />
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
