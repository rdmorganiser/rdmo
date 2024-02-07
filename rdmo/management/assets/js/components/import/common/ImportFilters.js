import React from 'react'
import PropTypes from 'prop-types'
import {FilterString, FilterUriPrefix} from '../../common/Filter'
import get from 'lodash/get'
import {getUriPrefixes} from '../../../utils/filter'
import {Checkbox} from '../../common/Checkboxes'

const ImportFilters = ({ config, elements, updatedAndChanged, configActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.import.elements.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.import.elements.uri_prefix', value)
  const updateFilterChanged = (value) => configActions.updateConfig('filter.import.elements.changed', value)

  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)

  const filterByChanged = (elements, selectFilterChanged) => {
    if (selectFilterChanged === true && updatedAndChanged.length > 0) {
    return updatedAndChanged
  } else {
    return elements
  }}
  const filterByUriSearch = (elements, searchString) => {
    if (searchString) {
      const lowercaseSearch = searchString.toLowerCase()
      return elements.filter((element) =>
        element.uri.toLowerCase().includes(lowercaseSearch)
          // || element.title.toLowerCase().includes(lowercaseSearch)
      )
    } else {
      return elements
    }
  }
    const filterByUriPrefix = (elements, searchUriPrefix) => {
    if (searchUriPrefix) {
      return elements.filter((element) =>
        element.uri_prefix.toLowerCase().includes(searchUriPrefix)
          // || element.title.toLowerCase().includes(lowercaseSearch)
      )
    } else {
      return elements
    }
  }
  const filteredElements = filterByUriSearch(
                                  filterByUriPrefix(
                                        filterByChanged(elements, selectFilterChanged),
                                  selectedUriPrefix),
                          searchString)


  return (
    <div className="row">
      <div className="row">
        <div className={'col-sm-8'}>
          <FilterString value={get(config, 'filter.import.elements.search', '')} onChange={updateFilterString}
                        placeholder={gettext('Filter uri')}/>
        </div>
        <div className="col-sm-4">
          <FilterUriPrefix value={get(config, 'filter.import.elements.uri_prefix', '')}
                           onChange={updateFilterUriPrefix}
                           options={getUriPrefixes(elements)}/>
        </div>
      </div>
      <div className="row-checkbox">
        {
          updatedAndChanged.length > 0 && <div className="checkboxes">
            <span className="mr-10">{gettext('Changed:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Filter changed')}</code>}
                      value={get(config, 'filter.import.elements.changed', false)} onChange={updateFilterChanged}/>
          </div>
        }
        {filteredElements.length}
      </div>
    </div>

)
}

ImportFilters.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  updatedAndChanged: PropTypes.array,
  configActions: PropTypes.object.isRequired,
}

export default ImportFilters
