import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import ImportElement from './ImportElement'
import ImportSuccessElement from './ImportSuccessElement'

import WarningsAggregated from './common/WarningsAggregated'
import ErrorsAggregated from './common/ErrorsAggregated'
import ImportInfo from './common/ImportInfo'
import ImportFilters from './common/ImportFilters'

import filterElements from '../../utils/importFilters'
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

  const filteredElements = filterElements(elements, selectFilterChanged, selectedUriPrefix, searchString)

  return (
    <div className='card'>
      <div className='card-header'>
        <div className='d-flex align-items-center gap-2'>
          <strong>{gettext('Import from')}</strong>
          <div className="flex-grow-1">
            <code className="code-import">{file.name}</code>
          </div>

          <ImportInfo elementsLength={elements.length} createdLength={createdElements.length}
                      updatedLength={updatedElements.length} changedLength={changedElements.length}
                      warningsLength={importWarnings.length} errorsLength={importErrors.length}/>
        </div>
      </div>
      <div className="card-body">
        <ImportFilters elements={elements} changedElements={changedElements}
                       filteredElements={filteredElements} success={success} />
        <WarningsAggregated elements={importWarnings} />
        <ErrorsAggregated elements={importErrors} />
      </div>
      <ul className='list-group list-group-flush'>
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
