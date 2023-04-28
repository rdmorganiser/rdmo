import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import Link from 'rdmo/core/assets/js/components/Link'

const ImportSidebar = ({ config, imports, importActions }) => {
  const count = imports.elements.filter(e => e.import).length
  const [uriPrefix, setUriPrefix] = useState('')
  const disabled = isNil(uriPrefix) || isEmpty(uriPrefix)

  const updateUriPrefix = () => {
    if (!disabled) {
      importActions.updateElements({uri_prefix: uriPrefix})
    }
  }

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
          <Link onClick={() => importActions.updateElements({import: true})}>
            {gettext('Select all')}
          </Link>
        </li>
        <li>
          <Link onClick={() => importActions.updateElements({import: false})}>
            {gettext('Unselect all')}
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
              onClick={event => setUriPrefix(config.settings.default_uri_prefix)}>
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

ImportSidebar.propTypes = {
  config: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSidebar
