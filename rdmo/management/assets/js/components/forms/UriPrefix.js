import React, { Component} from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const UriPrefix = ({ config, element, field, warnings, errors, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warningList = warnings[field],
        errorList = errors[field]

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warningList),
    'has-error': !isEmpty(errorList)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div className="input-group">
        <input className="form-control" id={id} type="text"
               value={value} onChange={event => onChange(field, event.target.value)} />

        <span className="input-group-btn">
          <button type="button" className="btn btn-default"
            title={gettext('Insert default URI Prefix')}
            onClick={event => onChange(field, config.settings.default_uri_prefix)}>
            <span className="fa fa-magic"></span>
          </button>
        </span>
      </div>

      {help && <p className="help-block">{help}</p>}

      {errorList && <ul className="help-block list-unstyled">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

UriPrefix.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  onChange: PropTypes.func
}

export default UriPrefix