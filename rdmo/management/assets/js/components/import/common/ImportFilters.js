import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { getUriPrefixes } from '../../../utils/filter'

import { FilterString, FilterUriPrefix } from '../../common/Filter'

const ImportFilters = ({ elements, changedElements, filteredElements, success = false }) => {
  const [filterString, setFilterString] = useConfig('filter.import.elements.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.import.elements.uri_prefix', '')
  const [filterChanged, setFilterChanged] = useConfig('filter.import.elements.changed', false)

  const updateFilterChanged = () => setFilterChanged(!filterChanged)

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
          <FilterString
            value={filterString} onChange={setFilterString}
            label={gettext('Filter URI')} />
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix
            value={filterUriPrefix}
            onChange={setFilterUriPrefix}
            options={getUriPrefixes(elements)} />
        </div>
      </div>
      {
        elements.length > 0 && (
          <>
            <div className="form-check mb-2">
              <input
                className="form-check-input" type="checkbox" id="import-filter-changed"
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
