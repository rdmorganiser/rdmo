import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

const UriPrefix = ({ config, element, onChange }) => {
  const id = uniqueId('uriPrefix-'),
        value = element.uri_prefix

  return (
    <div className="form-group mb-0">
      <label className="control-label" htmlFor={id}>
        <small>{gettext('URI prefix')}</small>
      </label>

      <div className="input-group">
        <input className="form-control input-sm" id={id} type="text"
               value={value} onChange={event => onChange('uri_prefix', event.target.value)} />

        <span className="input-group-btn">
          <button type="button" className="btn btn-default btn-sm"
            title={gettext('Insert default URI Prefix')}
            onClick={() => onChange('uri_prefix', config.settings.default_uri_prefix)}>
            <span className="fa fa-magic"></span>
          </button>
        </span>
      </div>
    </div>
  )
}

UriPrefix.propTypes = {
  config: PropTypes.object.isRequired,
  element: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired
}

export default UriPrefix
