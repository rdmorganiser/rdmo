import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import {Checkbox} from '../common/Checkboxes'


const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports
  const updateFilterString = (value) => configActions.updateConfig('filter.import.elements.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.import.elements.uri_prefix', value)
  const updateFilterChanged = (value) => configActions.updateConfig('filter.import.elements.changed', value)
  const updatedElements = elements.filter(element => element.updated)
  const createdElements = elements.filter(element => element.created)
  const updatedAndChangedElements = elements.filter(element => element.updated && !isEmpty(element.updated_and_changed))
  // const updatedAndSameElements = elements.filter(element => element.updated && isEmpty(element.updated_and_changed))
  const importErrors = elements.filter(element => !isEmpty(element.errors))
  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)
  const filterByChanged = (elements, selectFilterChanged) => {
    if (selectFilterChanged) {
    return updatedAndChangedElements
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
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')} from: {file.name}</strong>
        <div className="pull-right">
          {
            elements.length > 0 && <span>{gettext('Total')}: {elements.length} </span>
          }
          {
            updatedElements.length > 0 && <span> {gettext('Updated')}: {updatedElements.length}
            {' ('}{gettext('Changed')}: {updatedAndChangedElements.length}{') '}
              </span>
            }
          {
            createdElements.length > 0 && <span>{gettext('Created')}: {createdElements.length} </span>
          }
          {
            importErrors.length > 0 && <span>{gettext('Errors')}: {importErrors.length} </span>
          }
        </div>
      </div>
      <div className="panel-body">
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
        {
        updatedAndChangedElements.length > 0 && <div className="checkboxes">
          <span className="mr-10">{gettext('Changed:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Changed')}</code>}
                    value={get(config, 'filter.import.elements.changed', true)} onChange={updateFilterChanged}/>
        </div>
          }
      </div>
      <ul className="list-group">
        {
          filteredElements.map((element, index) => {
            if (success) {
              return <ImportSuccessElement key={index} element={element}/>
            } else {
              return <ImportElement key={index} config={config} element={element} importActions={importActions}/>
            }
          })
        }
      </ul>
    </div>
  )
}

Import.propTypes = {
  config: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default Import
