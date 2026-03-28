import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import uniqueId from 'lodash/uniqueId'

const UriPrefix = ({ element, onChange }) => {
  const config = useSelector((state) => state.config)

  const id = uniqueId('uriPrefix-')
  const value = element.uri_prefix

  return (
    <div className="mb-2">
      <label className="form-label" htmlFor={id}>
        <small>{gettext('URI prefix')}</small>
      </label>

      <div className="input-group">
        <input className="form-control input-sm" id={id} type="text"
          value={value} onChange={event => onChange('uri_prefix', event.target.value)} />

        <button type="button" className="btn btn-sm btn-light border"
          title={gettext('Insert default URI Prefix')} aria-label={gettext('Insert default URI Prefix')}
          onClick={() => onChange('uri_prefix', config.settings.default_uri_prefix)}>
          <span className="bi bi-magic"></span>
        </button>
      </div>
    </div>
  )
}

UriPrefix.propTypes = {
  element: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired
}

export default UriPrefix
