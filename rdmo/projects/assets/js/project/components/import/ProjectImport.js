import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'
import { useImportElements } from 'rdmo/management/assets/js/hooks/useImportElements'
import filterValues from 'rdmo/management/assets/js/utils/importFilters'

import ImportInfo from 'rdmo/management/assets/js/components/import/common/ImportInfo'

import ProjectImportFilter from './ProjectImportFilter'
import ProjectImportValue from './ProjectImportValue'

const ProjectImport = () => {
  const config = useSelector((state) => state.config)
  const { file, values } = useSelector((state) => state.projectImport)
  const {
    createdElements: createdValues,
    updatedElements: updatedValues,
    changedElements: changedValues,
    importWarnings,
    importErrors
  } = useImportElements(values)
  const searchString = get(config, 'filter.import.values.search', '')
  const selectedUriPrefix = get(config, 'filter.import.values.uri_prefix', '')
  const showOnlyChanged = isTruthy(get(config, 'filter.import.values.changed', false))
  const filteredValues = filterValues(values, showOnlyChanged, selectedUriPrefix, searchString)

  return (
    <div className="card">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong>{gettext('Import from')}</strong>
          <code className="code-import flex-grow-1">{file.name}</code>
          <ImportInfo
            elementsLength={values.length}
            createdLength={createdValues.length}
            updatedLength={updatedValues.length}
            changedLength={changedValues.length}
            warningsLength={importWarnings.length}
            errorsLength={importErrors.length}
          />
        </div>
      </div>
      <ProjectImportFilter
        values={values}
        changedValues={changedValues}
        filteredValues={filteredValues}
      />
      <ul className="list-group list-group-flush">
        {filteredValues.map(value => <ProjectImportValue key={value.key} value={value} />)}
      </ul>
    </div>
  )
}

export default ProjectImport
