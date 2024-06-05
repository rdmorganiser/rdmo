import React from 'react'
import PropTypes from 'prop-types'
import {FilterString, FilterUriPrefix} from '../../common/Filter'
import get from 'lodash/get'
import {getUriPrefixes} from '../../../utils/filter'
import {Checkbox} from '../../common/Checkboxes'

const ImportFilters = ({ config, elements, changedElements, filteredElements, configActions }) => {
  const updateFilterString = (value) => configActions.updateConfig('filter.import.elements.search', value)
  const getValueFilterString = () => get(config, 'filter.import.elements.search', '')
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.import.elements.uri_prefix', value)
  const getValueFilterUirPrefix = () => get(config, 'filter.import.elements.uri_prefix', '')
  const updateFilterChanged = (value) => configActions.updateConfig('filter.import.elements.changed', value)
  const getValueFilterChanged = () => get(config, 'filter.import.elements.changed', false)

  return (

      <div className="row">
        <div className={'col-sm-8'}>
          <FilterString value={getValueFilterString()} onChange={updateFilterString}
                        placeholder={gettext('Filter uri')}/>
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix value={getValueFilterUirPrefix()}
                           onChange={updateFilterUriPrefix}
                           options={getUriPrefixes(elements)}/>
        </div>

      {elements.length > 0 && (
        <div className="horizontal-container">
          <div className="checkboxes">
            <Checkbox label={interpolate(gettext('Show only created and changed (%s)'), [changedElements.length])}
                      value={getValueFilterChanged()} onChange={updateFilterChanged} />
          </div>
          <span className="shown-info">
            {gettext('Shown')}: {filteredElements.length} / {elements.length}
          </span>
        </div>
      )}
  </div>)
}

ImportFilters.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  changedElements: PropTypes.array.isRequired,
  filteredElements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
}

export default ImportFilters
