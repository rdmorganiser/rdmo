import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'

import Option from '../element/Option'
import OptionSet from '../element/OptionSet'

const NestedOptionSet = ({ optionset }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateFilterString = (uri) => dispatch(updateConfig('filter.optionset.search', uri))
  const updateFilterUriPrefix = (uriPrefix) => dispatch(updateConfig('filter.optionset.uri_prefix', uriPrefix))

  const displayUriOptions = isTruthy(get(config, 'display.uri.options', true))

  const toggleDisplayUriOptions = () => dispatch(updateConfig('display.uri.options', !displayUriOptions))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <>
      <div className="card">
        <div className="card-header">
          <OptionSet optionset={optionset} display="plain" backButton={true} />
        </div>

        <div className="card-body">
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
          <div className="input-group input-group-sm">
            <label className="input-group-text">{gettext('Show URIs')}</label>
            <button type="button" onClick={toggleDisplayUriOptions} className={btnClass(displayUriOptions)}>
              {gettext('Options')}
            </button>
          </div>
        </div>
      </div>

      {
        optionset.elements.map((option, index) => (
          <Option key={index} option={option} display="nested" filter="optionset" indent={1} />
        ))
      }
    </>
  )
}

NestedOptionSet.propTypes = {
  optionset: PropTypes.object.isRequired
}

export default NestedOptionSet
