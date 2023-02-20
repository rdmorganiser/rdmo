import React, { Component} from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'

import { getLabel, getHelp } from 'rdmo/management/assets/js/utils/meta'

const Text = ({ config, element, elementType, field, warnings, errors, onChange }) => {
  const id = `${elementType}-${field}`,
        value = element[field],
        label = getLabel(config, elementType, field),
        help = getHelp(config, elementType, field),
        warningList = warnings[field],
        errorList = errors[field]

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warningList),
    'has-error': !isEmpty(errorList)
  })

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <input className="form-control" id={id} type="text"
             value={value} onChange={event => onChange(field, event.target.value)} />

      {help && <p className="help-block">{help}</p>}

      {errorList && <ul className="help-block list-unstyled">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

Text.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  onChange: PropTypes.func
}

export default Text
