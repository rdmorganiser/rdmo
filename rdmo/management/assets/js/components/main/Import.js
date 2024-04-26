import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportWarningsPanel from '../import/ImportWarningsPanel'
import ImportErrorsPanel from '../import/ImportErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportFilters'
import useFilteredElements from '../../utils/importFilters'
import {useImportElements} from '../../hooks/useImportElements'


const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports

   const {
    elementsImported,
    createdElements,
    updatedElements,
    changedElements,
    importWarnings,
    importErrors
  } = useImportElements(elements)

  const searchString = get(config, 'filter.import.elements.search', '')
  const selectedUriPrefix = get(config, 'filter.import.elements.uri_prefix', '')
  const selectFilterChanged = get(config, 'filter.import.elements.changed', false)

  const filteredElements = useFilteredElements(elementsImported, selectFilterChanged, selectedUriPrefix, searchString)

  return (
    <div className='panel panel-default panel-import'>
      <div className='panel-heading'>
        <strong>{gettext('Import')} from: {file.name}</strong>
        <ImportInfo elementsLength={elementsImported.length} createdLength={createdElements.length}
                        updatedLength={updatedElements.length} changedLength={changedElements.length}
                        warningsLength={importWarnings.length} errorsLength={importErrors.length}/>

      </div>
        {
          changedElements.length > 0 &&
          <ImportFilters config={config} elements={elementsImported}
                         updatedAndChanged={changedElements}
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
        <ul className='list-group'>
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
