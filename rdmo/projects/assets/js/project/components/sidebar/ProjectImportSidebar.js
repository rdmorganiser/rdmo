import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { useImportElements } from 'rdmo/management/assets/js/hooks/useImportElements'

import {
  resetValues,
  selectChangedValues,
  selectValues,
  showChangedValues,
  showValues
} from '../../actions/importActions'

const ProjectImportSidebar = () => {
  const dispatch = useDispatch()
  const values = useSelector((state) => state.projectImport.values)
  const { changedElements: changedValues } = useImportElements(values)
  const importValues = values.filter(value => value.import)
  const count = importValues.length
  const handleImport = () => {
    const payload = {
      values: importValues
    }

    console.log('Project import payload', payload)
  }

  return (
    <div className="project-import-sidebar">
      <div className="px-3 my-4">
        <h3>{gettext('Import values')}</h3>
        <p className="text-muted">{gettext('Preview using example project data.')}</p>
      </div>

      <div className="d-flex align-items-center gap-2 px-3 my-3">
        <button
          type="button"
          className="btn btn-success flex-grow-1"
          disabled={count === 0}
          onClick={handleImport}
        >
          {interpolate(ngettext('Import one value', 'Import %s values', count), [count])}
        </button>
        <button
          type="button"
          className="btn btn-light border"
          onClick={() => dispatch(resetValues())}
        >
          {gettext('Back')}
        </button>
      </div>

      <div className="px-3 my-4">
        <h3>{gettext('Selection')}</h3>
      </div>

      <div className="d-flex flex-column gap-2 px-3 my-3">
        <button
          type="button"
          className="btn btn-light border text-start"
          onClick={() => dispatch(selectValues(true))}
        >
          {gettext('Select all')}
        </button>
        {
          changedValues.length > 0 && (
            <button
              type="button"
              className="btn btn-light border text-start"
              onClick={() => dispatch(selectChangedValues(true))}
            >
              {gettext('Select new and changed')}
            </button>
          )
        }
        <button
          type="button"
          className="btn btn-light border text-start"
          onClick={() => dispatch(selectValues(false))}
        >
          {gettext('Deselect all')}
        </button>
        {
          changedValues.length > 0 && (
            <button
              type="button"
              className="btn btn-light border text-start"
              onClick={() => dispatch(selectChangedValues(false))}
            >
              {gettext('Deselect new and changed')}
            </button>
          )
        }
      </div>

      <div className="px-3 my-4">
        <h3>{gettext('Details')}</h3>
      </div>

      <div className="d-flex flex-column gap-2 px-3 my-4">
        <button
          type="button"
          className="btn btn-light border text-start"
          onClick={() => dispatch(showValues(true))}
        >
          {gettext('Expand all')}
        </button>
        {
          changedValues.length > 0 && (
            <button
              type="button"
              className="btn btn-light border text-start"
              onClick={() => dispatch(showChangedValues(true))}
            >
              {gettext('Expand new and changed')}
            </button>
          )
        }
        <button
          type="button"
          className="btn btn-light border text-start"
          onClick={() => dispatch(showValues(false))}
        >
          {gettext('Collapse all')}
        </button>
        {
          changedValues.length > 0 && (
            <button
              type="button"
              className="btn btn-light border text-start"
              onClick={() => dispatch(showChangedValues(false))}
            >
              {gettext('Collapse new and changed')}
            </button>
          )
        }
      </div>
    </div>
  )
}

export default ProjectImportSidebar
