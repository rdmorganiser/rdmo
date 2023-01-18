import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Option from '../element/Option'

const Options = ({ config, options, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.options.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.options.uri_prefix', value)
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
            <FilterString value={config.filter.options.search} onChange={updateFilterString}
                          placeholder={gettext('Filter options')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.options.uri_prefix} onChange={updateFilterUriPrefix}
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