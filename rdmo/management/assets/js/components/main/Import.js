import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportAggregatedWarningsPanel from '../import/ImportAggregatedWarningsPanel'
import ImportAggregatedErrorsPanel from '../import/ImportAggregatedErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportFilters'
import useFilteredElements from '../../utils/importFilters'
import {useImportElements} from '../../hooks/useImportElements'


const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports
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
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)

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
        {
          <ImportFilters config={config} elements={elements}
                         changedElements={changedElements}
                         filteredElements={filteredElements}
                         configActions={configActions}
                         success={success} />
        }
        {
          <ImportAggregatedWarningsPanel config={config} elements={importWarnings}
                                         importActions={importActions}
                                         configActions={configActions} />
        }
        {
          <ImportAggregatedErrorsPanel config={config} elements={importErrors}
                                       importActions={importActions}
                                       configActions={configActions} />
        }
      </div>
        <ul className='list-group'>
          {
            filteredElements.map((element, index) => {
              if (success) {
                return <ImportSuccessElement key={index} element={element}
                                             importActions={importActions}/>
              } else {
                return <ImportElement key={index} element={element} config={config}
                                      importActions={importActions}/>
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
