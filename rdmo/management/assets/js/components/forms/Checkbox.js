import React, { Component} from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'

import { getLabel, getHelp } from 'rdmo/management/assets/js/utils/meta'

const Checkbox = ({ config, element, elementType, field, warnings, errors, onChange }) => {
  const id = `${elementType}-${field}`,
        checked = element[field],
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
      <div className="checkbox">
          <label>
              <input id={id} type="checkbox" checked={checked}
                     onChange={event => onChange(field, !checked)} />
              <span>{label}</span>
          </label>
      </div>

      {help && <p className="help-block">{help}</p>}

      {errorList && <ul className="help-block list-unstyled">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

Checkbox.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  onChange: PropTypes.func,
}

export default Checkbox
