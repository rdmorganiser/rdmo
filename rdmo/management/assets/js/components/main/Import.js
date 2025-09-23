import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportAggregatedWarningsPanel from '../import/ImportAggregatedWarningsPanel'
import ImportAggregatedErrorsPanel from '../import/ImportAggregatedErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportFilters'
import useFilteredElements from '../../utils/importFilters'
import { useImportElements } from '../../hooks/useImportElements'


const Import = () => {
  const config = useSelector((state) => state.config)
  const { file, elements, success } = useSelector((state) => state.imports)

  // the elements are already processed by processElementDiffs in the importsReducer
  const {
    createdElements,
    updatedElements,
    changedElements,
    importWarnings,
    importErrors
  } = useImportElements(elements)

  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = isTruthy(get(config, 'filter.import.elements.changed', false))

  const filteredElements = useFilteredElements(elements, selectFilterChanged, selectedUriPrefix, searchString)

  return (
    <div className='panel panel-default panel-import'>
      <div className='panel-heading'>
        <strong>{gettext('Import')} from: {file.name}</strong>

        <ImportInfo elementsLength={elements.length} createdLength={createdElements.length}
                    updatedLength={updatedElements.length} changedLength={changedElements.length}
                    warningsLength={importWarnings.length} errorsLength={importErrors.length}/>

      </div>
      <div className="panel-body">
        <ImportFilters elements={elements} changedElements={changedElements}
                       filteredElements={filteredElements} success={success} />
        <ImportAggregatedWarningsPanel elements={importWarnings} />
        <ImportAggregatedErrorsPanel elements={importErrors} />
      </div>
        <ul className='list-group'>
          {
            filteredElements.map((element, index) => {
              if (success) {
                return <ImportSuccessElement key={index} element={element} />
              } else {
                return <ImportElement key={index} element={element} />
              }
            })
          }
        </ul>
  </div>
  )
}

export default Import
