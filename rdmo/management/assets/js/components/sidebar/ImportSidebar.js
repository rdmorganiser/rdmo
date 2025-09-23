import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import Link from 'rdmo/core/assets/js/components/Link'

import { resetElements, importElements, selectElements, selectChangedElements,
         showElements, showChangedElements } from '../../actions/importActions'

import {useImportElements} from '../../hooks/useImportElements'


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

  const updateUriPrefix = () => {
    if (!disabled) {
      dispatch(updateUriPrefix(uriPrefix))
    }
  }

  if (success) {
    return (
      <div className="import-sidebar">
        <h2>{gettext('Import successful')}</h2>

        <p className="import-buttons">
          <button type="button" className="btn btn-default" onClick={() => dispatch(resetElements())}>
            {gettext('Back')}
          </button>
        </p>
      </div>
    )
  } else {
    return (
      <div className="import-sidebar">
        <h2>{gettext('Import elements')}</h2>
        <p className="import-buttons">
          <button type="button" className="btn btn-success" onClick={() => dispatch(importElements())}>
            {interpolate(ngettext('Import one element', 'Import %s elements', count), [count])}
          </button>
          <button type="button" className="btn btn-default" onClick={() => dispatch(resetElements())}>
            {gettext('Back')}
          </button>
        </p>

        <h2>{gettext('Selection')}</h2>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => dispatch(selectElements(true))}>
              {gettext('Select all')}
            </Link>
          </li>
          {changedElements.length > 0 &&
            <li>
              <Link onClick={() => dispatch(selectChangedElements(true))}>
                {gettext('Select changed')}
              </Link>
            </li>
          }
          <li>
            <Link onClick={() => dispatch(selectElements(false))}>
              {gettext('Deselect all')}
            </Link>
          </li>
          {changedElements.length > 0 &&
            <li>
              <Link onClick={() => dispatch(selectChangedElements(false))}>
                {gettext('Deselect changed')}
              </Link>
            </li>
          }
        </ul>

          <h2>{gettext('Show')}</h2>
          <ul className="list-unstyled">
          <li>
            <Link onClick={() => dispatch(showElements(true))}>
              {gettext('Show all')}
            </Link>
          </li>
          {changedElements.length > 0 &&
            <li>
              <Link onClick={() => dispatch(showChangedElements(true))}>
                {gettext('Show changes')}
              </Link>
            </li>
          }
          <li>
            <Link onClick={() => dispatch(showElements(false))}>
              {gettext('Hide all')}
            </Link>
          </li>
            {changedElements.length > 0 &&
              <li>
                <Link onClick={() => dispatch(showChangedElements(false))}>
                  {gettext('Hide changes')}
                </Link>
              </li>
            }
          </ul>

        <h2>{gettext('URI prefix')}</h2>

        <div className="form-group">
          <div className="input-group">
            <input className="form-control" type="text"
                   placeholder={gettext('URI prefix')} aria-label={gettext('URI prefix')}
                   value={uriPrefix} onChange={event => setUriPrefix(event.target.value)} />

            <span className="input-group-btn">
              <button type="button" className="btn btn-default"
                title={gettext('Insert default URI Prefix')}
                aria-label={gettext('Insert default URI Prefix')}
                onClick={() => setUriPrefix(settings.default_uri_prefix)}>
                <span className="fa fa-magic"></span>
              </button>
              <button type="button" className="btn btn-primary" disabled={disabled}
                title={gettext('Set URI prefix for all elements')}
                aria-label={gettext('Set URI prefix for all elements')}
                onClick={updateUriPrefix}>
                <span className="fa fa-arrow-right"></span>
              </button>
            </span>
          </div>
        </div>
      </div>
    )
  }
}

export default ImportSidebar
