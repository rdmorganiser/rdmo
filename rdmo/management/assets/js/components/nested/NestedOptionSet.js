import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'

import Option from '../element/Option'
import OptionSet from '../element/OptionSet'

const NestedOptionSet = ({ config, optionset, configActions, elementActions }) => {

  const updateFilterString = (uri) => configActions.updateConfig('filter.optionset.search', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.optionset.uri_prefix', uriPrefix)

  const updateDisplayURI = (value) => configActions.updateConfig('display.uri.options', value)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <OptionSet config={config} optionset={optionset}
                     configActions={configActions} elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.optionset.search', '')} onChange={updateFilterString}
                            label={gettext('Filter option sets')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.optionset.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(optionset.elements)} />
            </div>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-options">{gettext('Options')}</code>}
                      value={get(config, 'display.uri.options', true)} onChange={updateDisplayURI} />
          </div>
        </div>
      </div>

      {
        optionset.elements.map((option, index) => (
          <Option key={index} config={config} option={option}
                  configActions={configActions} elementActions={elementActions}
                  display="nested" filter="optionset" indent={1} />
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
