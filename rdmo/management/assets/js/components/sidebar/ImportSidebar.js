import React, { useState } from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import Link from 'rdmo/core/assets/js/components/Link'
import {useImportElements} from '../../hooks/useImportElements'


const ImportSidebar = ({ config, imports, importActions }) => {
  const { elements, success } = imports

   const {
    // elementsImported,
    // createdElements,
    // updatedElements,
    changedElements,
    // importWarnings,
    // importErrors
  } = useImportElements(elements)

  const count = elements.filter(e => e.import).length
  const [uriPrefix, setUriPrefix] = useState('')
  const disabled = isNil(uriPrefix) || isEmpty(uriPrefix)

  const updateUriPrefix = () => {
    if (!disabled) {
      importActions.updateUriPrefix(uriPrefix)
    }
  }

  if (success) {
    return (
      <div className="import-sidebar">
        <h2>{gettext('Import successful')}</h2>

        <p className="import-buttons">
          <button className="btn btn-default" onClick={() => importActions.resetElements()}>
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
          <button className="btn btn-success" onClick={() => importActions.importElements()}>
            {interpolate(ngettext('Import one element', 'Import %s elements', count), [count])}
          </button>
          <button className="btn btn-default" onClick={() => importActions.resetElements()}>
            {gettext('Back')}
          </button>
        </p>

        <h2>{gettext('Selection')}</h2>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => importActions.selectElements(true)}>
              {gettext('Select all')}
            </Link>
          </li>
            {changedElements.length > 0 &&
            <li>
              <ul className="list-unstyled" style={{paddingLeft:'20px'}}>
                <li>
                  <Link onClick={() => importActions.selectChangedElements(true)}>
                    {gettext('Select changed')}
                  </Link>
                </li>
                <li>
                  <Link onClick={() => importActions.selectChangedElements(false)}>
                    {gettext('Unselect changed')}
                  </Link>
                </li>
              </ul>
            </li>
            }
          <li>
            <Link onClick={() => importActions.selectElements(false)}>
              {gettext('Unselect all')}
            </Link>
          </li>
          </ul>

          <h2>{gettext('Show')}</h2>
          <ul className="list-unstyled">
          <li>
            <Link onClick={() => importActions.showElements(true)}>
              {gettext('Show all')}
            </Link>
          </li>
          {changedElements.length > 0 &&
              <li>
                <ul className="list-unstyled" style={{paddingLeft:'20px'}}>
                  <li>
                    {/* TODO fix action showChangedElements */}
                    <Link onClick={() => importActions.showChangedElements(true)}>
                      {gettext('Show changes')}
                    </Link>
                  </li>
                  <li>
                    {/* TODO fix action showChangedElements */}
                    <Link onClick={() => importActions.showChangedElements(false)}>
                      {gettext('Hide changes')}
                    </Link>
                  </li>
                </ul>
              </li>
          }
          <li>
            <Link onClick={() => importActions.showElements(false)}>
              {gettext('Hide all')}
            </Link>
          </li>
        </ul>

        <h2>{gettext('URI prefix')}</h2>

        <div className="form-group">
          <div className="input-group">
            <input className="form-control" type="text" placeholder={gettext('URI prefix')}
                   value={uriPrefix} onChange={event => setUriPrefix(event.target.value)} />

            <span className="input-group-btn">
              <button type="button" className="btn btn-default"
                title={gettext('Insert default URI Prefix')}
                onClick={() => setUriPrefix(config.settings.default_uri_prefix)}>
                <span className="fa fa-magic"></span>
              </button>
              <button type="button" className="btn btn-primary" disabled={disabled}
                title={gettext('Set URI prefix for all elements')}
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

ImportSidebar.propTypes = {
  config: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSidebar
