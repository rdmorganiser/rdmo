import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { getUriPrefixes } from '../../../utils/filter'

import { FilterString, FilterUriPrefix } from '../../common/Filter'

const ImportFilters = ({ elements, changedElements, filteredElements, success = false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const filterString = get(config, 'filter.import.elements.search', '')
  const filterUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const filterChanged = isTruthy(get(config, 'filter.import.elements.changed', false))

  const updateFilterString = (value) => dispatch(updateConfig('filter.import.elements.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.import.elements.uri_prefix', value))
  const updateFilterChanged = () => dispatch(updateConfig('filter.import.elements.changed', !filterChanged))

  const filterCheckBoxText = interpolate(
    success ? (
      gettext('Show only created and changed elements (%s)')
    ) : gettext('Show only new and changed elements (%s)'),
    [changedElements.length]
  )

  return !isEmpty(elements) && (
    <>
      <div className="row">
        <div className={'col-sm-8'}>
          <FilterString value={filterString} onChange={updateFilterString}
            label={gettext('Filter URI')} />
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix value={filterUriPrefix}
            onChange={updateFilterUriPrefix}
            options={getUriPrefixes(elements)} />
        </div>
      </div>
      {
        elements.length > 0 && (
          <>
            <div className="form-check mb-2">
              <input className="form-check-input" type="checkbox" id="import-filter-changed"
                checked={filterChanged} onChange={updateFilterChanged} />
              <label className="form-check-label" htmlFor="import-filter-changed">
                {filterCheckBoxText}
              </label>
            </div>
            <div>
              {gettext('Shown')}: {filteredElements.length} / {elements.length}
            </div>
          </>
        )
      }
    </>
  )
}

ImportFilters.propTypes = {
  elements: PropTypes.array.isRequired,
  changedElements: PropTypes.array.isRequired,
  filteredElements: PropTypes.array.isRequired,
  success: PropTypes.bool
}

export default ImportFilters
