import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

const UriPath = ({ element, onChange }) => {
  const id = uniqueId('uriPath-'),
        value = element.uri_path ?? ''

  return (
    <div className="form-group mb-0">
      <label className="control-label" htmlFor={id}>
        <small>{gettext('URI path')}</small>
      </label>

      <input className="form-control input-sm" id={id} type="text"
             value={value} onChange={event => onChange('uri_path', event.target.value)} />
    </div>
  )
}

UriPath.propTypes = {
  element: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired
}

export default UriPath
