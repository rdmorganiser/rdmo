import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'
import { getUriPrefixes } from 'rdmo/management/assets/js/utils/filter'

import { FilterString, FilterUriPrefix } from 'rdmo/management/assets/js/components/common/Filter'

const ProjectImportFilter = ({ values, changedValues, filteredValues }) => {
  const dispatch = useDispatch()
  const config = useSelector((state) => state.config)

  const searchString = get(config, 'filter.import.values.search', '')
  const selectedUriPrefix = get(config, 'filter.import.values.uri_prefix', '')
  const showOnlyChanged = isTruthy(get(config, 'filter.import.values.changed', false))

  const updateSearchString = (value) => dispatch(updateConfig('filter.import.values.search', value))
  const updateUriPrefix = (value) => dispatch(updateConfig('filter.import.values.uri_prefix', value))
  const updateChanged = () => dispatch(updateConfig('filter.import.values.changed', !showOnlyChanged))

  return (
    <div className="card-body">
      <div className="row">
        <div className="col-sm-8">
          <FilterString
            value={searchString}
            onChange={updateSearchString}
            label={gettext('Filter URI')}
          />
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix
            value={selectedUriPrefix}
            onChange={updateUriPrefix}
            options={getUriPrefixes(values)}
          />
        </div>
      </div>
      <div className="form-check mb-2">
        <input
          className="form-check-input"
          type="checkbox"
          id="project-import-filter-changed"
          checked={showOnlyChanged}
          onChange={updateChanged}
        />
        <label className="form-check-label" htmlFor="project-import-filter-changed">
          {
            interpolate(
              gettext('Show only new and changed values (%s)'),
              [changedValues.length]
            )
          }
        </label>
      </div>
      <div>{gettext('Shown')}: {filteredValues.length} / {values.length}</div>
    </div>
  )
}

ProjectImportFilter.propTypes = {
  values: PropTypes.array.isRequired,
  changedValues: PropTypes.array.isRequired,
  filteredValues: PropTypes.array.isRequired
}

export default ProjectImportFilter
