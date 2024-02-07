import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import ImportElement from '../import/ImportElement'
import ImportSuccessElement from '../import/ImportSuccessElement'
import ImportWarningsPanel from '../import/ImportWarningsPanel'
import ImportErrorsPanel from '../import/ImportErrorsPanel'
import ImportInfo from '../import/common/ImportInfo'
import ImportFilters from '../import/common/ImportInfo'


const Import = ({ config, imports, configActions, importActions }) => {
  const { file, elements, success } = imports

  const updatedAndChangedElements = elements.filter(element => element.updated && !isEmpty(element.updated_and_changed))

  const updatedElements = elements.filter(element => element.updated)
  const createdElements = elements.filter(element => element.created)

  const importWarnings = elements.filter(element => !isEmpty(element.warnings))
  const importErrors = elements.filter(element => !isEmpty(element.errors))

  const filteredElements = elements

  return (
    <div className="panel panel-default panel-import">
      <div className="panel-heading">
        <strong>{gettext('Import')} from: {file.name}</strong>
        <ImportInfo elementsLength={elements.length} createdLength={createdElements.length}
                        updatedLength={updatedElements.length} changedLength={updatedAndChangedElements.length}
                        warningsLength={importWarnings.length} errorsLength={importErrors.length}/>

      </div>
      <div className="panel-body">
        <ImportFilters config={config} elements={elements} updatedAndChanged={updatedAndChangedElements}
                         importActions={importActions} configActions={configActions}/>

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
