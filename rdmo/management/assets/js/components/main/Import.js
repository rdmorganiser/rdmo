import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportWarningsPanel from '../import/ImportWarningsPanel'
import ImportErrorsPanel from '../import/ImportErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportFilters'
import get from 'lodash/get'

const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports

  const updatedAndChangedElements = elements.filter(element => element.updated && !isEmpty(element.updated_and_changed))

  const updatedElements = elements.filter(element => element.updated)
  const createdElements = elements.filter(element => element.created)

  const importWarnings = elements.filter(element => !isEmpty(element.warnings))
  const importErrors = elements.filter(element => !isEmpty(element.errors))

  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)

  // filter func callbacks
  const filterByChanged = (elements, selectFilterChanged, updatedAndChangedElements) => {
    if (selectFilterChanged === true && updatedAndChangedElements.length > 0) {
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
                                        filterByChanged(elements, selectFilterChanged, updatedAndChangedElements),
                                  selectedUriPrefix),
                          searchString)

  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')} from: {file.name}</strong>
        <ImportInfo elementsLength={elements.length} createdLength={createdElements.length}
                        updatedLength={updatedElements.length} changedLength={updatedAndChangedElements.length}
                        warningsLength={importWarnings.length} errorsLength={importErrors.length}/>

      </div>
        {
          updatedAndChangedElements.length > 0 &&
          <ImportFilters config={config} elements={elements}
                         updatedAndChanged={updatedAndChangedElements}
                         filteredElements={filteredElements}
                         configActions={configActions}
          />
        }

        {
        importWarnings.length > 0 &&
          <ImportWarningsPanel config={config} elements={importWarnings} importActions={importActions}
                               configActions={configActions}/>
        }
        {
        importErrors.length > 0 &&
          <ImportErrorsPanel config={config} elements={importErrors} importActions={importActions}
                               configActions={configActions}/>
        }
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
