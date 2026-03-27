import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import {
  importElements, resetElements, selectChangedElements,
  selectElements, showChangedElements,          showElements, updateUriPrefix 
} from '../../actions/importActions'
import { useImportElements } from '../../hooks/useImportElements'


const ImportSidebar = () => {
  const dispatch = useDispatch()

  const { settings } = useSelector((state) => state.config)
  const { elements, success } = useSelector((state) => state.imports)

  const {
    changedElements,
  } = useImportElements(elements)

  const count = elements.filter(e => e.import).length
  const [uriPrefix, setUriPrefix] = useState('')
  const disabled = isNil(uriPrefix) || isEmpty(uriPrefix)

  const handleUpdateUriPrefix = () => {
    if (!disabled) {
      dispatch(updateUriPrefix(uriPrefix))
    }
  }

  if (success) {
    return (
      <div className="import-sidebar">
        <h2>{gettext('Import successful')}</h2>

        <p className="import-buttons">
          <button type="button" className="btn btn-light border" onClick={() => dispatch(resetElements())}>
            {gettext('Back')}
          </button>
        </p>
      </div>
    )
  } else {
    return (
      <div className="import-sidebar">

        <div className="px-3 my-4">
          <h3>{gettext('Import elements')}</h3>
        </div>

        <div className="d-flex align-items-center gap-2 px-3 my-3">
          <button type="button" className="btn btn-success flex-grow-1" onClick={() => dispatch(importElements())}>
            {interpolate(ngettext('Import one element', 'Import %s elements', count), [count])}
          </button>
          <button type="button" className="btn btn-light border" onClick={() => dispatch(resetElements())}>
            {gettext('Back')}
          </button>
        </div>

        <div className="px-3 my-4">
          <h3>{gettext('Selection')}</h3>
        </div>

        <div className="d-flex flex-column gap-2 px-3 my-3">
          <button type="button" className="btn btn-light border text-start"
            onClick={() => dispatch(selectElements(true))}>
            {gettext('Select all')}
          </button>
          {
            changedElements.length > 0 && (
              <button type="button" className="btn btn-light border text-start"
                onClick={() => dispatch(selectChangedElements(true))}>
                {gettext('Select changed')}
              </button>
            )
          }
          <button type="button" className="btn btn-light border text-start"
            onClick={() => dispatch(selectElements(false))}>
            {gettext('Deselect all')}
          </button>
          {
            changedElements.length > 0 && (
              <button type="button" className="btn btn-light border text-start"
                onClick={() => dispatch(selectChangedElements(false))}>
                {gettext('Deselect changed')}
              </button>
            )
          }
        </div>

        <div className="px-3 my-4">
          <h3>{gettext('Show')}</h3>
        </div>

        <div className="d-flex flex-column gap-2 px-3 my-4">
          <button type="button" className="btn btn-light border text-start"
            onClick={() => dispatch(showElements(true))}>
            {gettext('Show all')}
          </button>
          {
            changedElements.length > 0 && (
              <button type="button" className="btn btn-light border text-start"
                onClick={() => dispatch(showChangedElements(true))}>
                {gettext('Show changes')}
              </button>
            )
          }
          <button type="button" className="btn btn-light border text-start"
            onClick={() => dispatch(showElements(false))}>
            {gettext('Hide all')}
          </button>
          {
            changedElements.length > 0 && (
              <button type="button" className="btn btn-light border text-start"
                onClick={() => dispatch(showChangedElements(false))}>
                {gettext('Hide changes')}
              </button>
            )
          }
        </div>

        <div className="px-3 my-4">
          <h3>{gettext('URI prefix')}</h3>

          <div className="input-group">
            <input type="text" className="form-control"
              placeholder={gettext('URI prefix')} aria-label={gettext('URI prefix')}
              value={uriPrefix} onChange={event => setUriPrefix(event.target.value)} />

            <button type="button" className="btn btn-light border"
              title={gettext('Insert default URI Prefix')}
              aria-label={gettext('Insert default URI Prefix')}
              onClick={() => setUriPrefix(settings.default_uri_prefix)}>
              <span className="bi bi-magic"></span>
            </button>

            <button type="button" className="btn btn-primary" disabled={disabled}
              title={gettext('Set URI prefix for all elements')}
              aria-label={gettext('Set URI prefix for all elements')}
              onClick={handleUpdateUriPrefix}>
              <span className="bi bi-arrow-right"></span>
            </button>
          </div>
        </div>
      </div>
    )
  }
}

export default ImportSidebar
