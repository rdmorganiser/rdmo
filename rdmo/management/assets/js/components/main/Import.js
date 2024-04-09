import React from 'react'
import isEmpty from 'lodash/isEmpty'
import { DiffMethod } from 'react-diff-viewer-continued'
import PropTypes from 'prop-types'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportWarningsPanel from '../import/ImportWarningsPanel'
import ImportErrorsPanel from '../import/ImportErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportFilters'
import get from 'lodash/get'

function getDiffData( diffData ) {
    const OriginalValue = diffData.current_data || ''
    const NewValue = diffData.new_data || ''

  let OriginalValueStr = OriginalValue
  let NewValueStr = NewValue
    if (Array.isArray(NewValue) && Array.isArray(OriginalValue)) {
      // cast Array to String, joined by newline
      OriginalValueStr = OriginalValue.join('\n')
      NewValueStr = NewValue.join('\n')
      console.log('isArray', NewValue, OriginalValueStr, NewValueStr)
      diffData.hideLineNumbers = false
      diffData.splitView = false
      diffData.compareMethod = DiffMethod.LINES
    }
    else {
      OriginalValueStr = OriginalValue.toString()
      NewValueStr = NewValue.toString()
    }
    const equality = NewValueStr === OriginalValueStr
    diffData.changed = !equality
    diffData.newValue = NewValueStr
    diffData.oldValue = OriginalValueStr
    return diffData

}

function getDiffsForUpdatedElement( element )  {
  let changedElement = false
  let changedFields = []
  Object.entries(element.updated_and_changed).sort().map(([key, diffData]) => {
    const elementFieldDiff = getDiffData(diffData)
    console.log('setDiffsAllFields', key, elementFieldDiff)
    if (elementFieldDiff.changed ?? true) {
      changedFields.push(key)
      changedElement = true
    }
    element.updated_and_changed[key] = elementFieldDiff
  })
  element.changedFields = changedFields
  element.changed = changedElement
  // this.element.updated_and_changed = updatedAndChangedElement
  return element
}


class ImportedElementsDiffsManager {
  constructor( elements ) {
    // Assign the RGB values as a property of `this`.
    this.elementsImported = elements
    this.elements = []
    this.createdElements = []
    this.updatedElements = []
    this.changedElements = []
    this.importWarnings = []
    this.importErrors = []
  }
  setElementsDiff() {
    this.elementsImported.forEach(elementRaw => {
      const element = getDiffsForUpdatedElement(elementRaw)
      this.elements.push(element)
      if (element.updated ?? true) {
        this.updatedElements.push(element)
        if (element.changed ?? true) {
          this.changedElements.push(element)
        }
      } else {
        if (element.created ?? true) {
          this.createdElements.push(element)
          }
        }
      if (!isEmpty(element.warnings)) {
        this.importWarnings.push(element)
      }
      if (!isEmpty(element.errors)) {
        this.importErrors.push(element)
      }
      })
    }
}

function filterElementsByChanged (elements, selectFilterChanged) {
    if (selectFilterChanged === true) {
      return elements.filter((element) => element.changed)
  } else {
    return elements
  }}

function filterElementsByUri (elements, searchString) {
  if (searchString) {
    const lowercaseSearch = searchString.toLowerCase()
    return elements.filter((element) =>
      element.uri.toLowerCase().includes(lowercaseSearch)
    )} else {
    return elements
  }
}

function filterElementsByUriPrefix(elements, searchUriPrefix) {
    if (searchUriPrefix) {
      return elements.filter((element) =>
        element.uri_prefix.toLowerCase().includes(searchUriPrefix)
      )} else {
        return elements
      }
    }

function filterElements(elements, selectFilterChanged, selectedUriPrefix, searchString) {
  const filteredElements = filterElementsByUri(
    filterElementsByUriPrefix(
      filterElementsByChanged(elements, selectFilterChanged),
      selectedUriPrefix),
    searchString)
  return filteredElements
}

const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports

  const elementsDiff = new ImportedElementsDiffsManager(elements)
  elementsDiff.setElementsDiff()

  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)

  const filteredElements = filterElements(elements, selectFilterChanged, selectedUriPrefix, searchString)

  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')} from: {file.name}</strong>
        <ImportInfo elementsLength={elementsDiff.elements.length} createdLength={elementsDiff.createdElements.length}
                        updatedLength={elementsDiff.updatedElements.length} changedLength={elementsDiff.changedElements.length}
                        warningsLength={elementsDiff.importWarnings.length} errorsLength={elementsDiff.importErrors.length}/>

      </div>
        {
          elementsDiff.changedElements.length > 0 &&
          <ImportFilters config={config} elements={elementsDiff.elements}
                         updatedAndChanged={elementsDiff.changedElements}
                         filteredElements={filteredElements}
                         configActions={configActions}
          />
        }

        {
        elementsDiff.importWarnings.length > 0 &&
          <ImportWarningsPanel config={config} elements={elementsDiff.importWarnings} importActions={importActions}
                               configActions={configActions}/>
        }
        {
        elementsDiff.importErrors.length > 0 &&
          <ImportErrorsPanel config={config} elements={elementsDiff.importErrors} importActions={importActions}
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
