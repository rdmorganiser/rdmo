import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const UriPrefix = ({ config, element, field, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warnings = get(element, ['warnings', field]),
        errors = get(element, ['errors', field])

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warnings),
    'has-error': !isEmpty(errors)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div className="input-group">
        <input className="form-control" id={id} type="text" disabled={element.read_only}
               value={value} onChange={event => onChange(field, event.target.value)} />

        <span className="input-group-btn">
          <button type="button" className="btn btn-default" disabled={element.read_only}
            title={gettext('Insert default URI Prefix')}
            onClick={() => onChange(field, config.settings.default_uri_prefix)}>
            <span className="fa fa-magic"></span>
          </button>
        </span>
      </div>

      {help && <p className="help-block">{help}</p>}

      {errors && <ul className="help-block list-unstyled">
        {errors.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

UriPrefix.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default UriPrefix
