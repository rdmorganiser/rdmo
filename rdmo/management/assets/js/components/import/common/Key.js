import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

const Key = ({ element, onChange }) => {
  const id = uniqueId('key-'),
        value = element.key ?? ''

  return (
    <div className="form-group mb-0">
      <label className="control-label" htmlFor={id}>
        <small>{gettext('Key')}</small>
      </label>

      <input className="form-control input-sm" id={id} type="text"
             value={value} onChange={event => onChange('key', event.target.value)} />
    </div>
  )
}

Key.propTypes = {
  element: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired
}

export default Key
