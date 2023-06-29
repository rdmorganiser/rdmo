import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const Checkbox = ({ config, element, field, onChange }) => {
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

  const checked = isNil(element[field]) ? '' : element[field]

  return (
    <div className={className}>
      <div className="checkbox">
          <label>
              <input id={id} type="checkbox" checked={checked} disabled={element.read_only}
                     onChange={() => onChange(field, !checked)} />
              <span>{label}</span>
          </label>
      </div>

      {help && <p className="help-block">{help}</p>}

      {errors && <ul className="help-block list-unstyled">
        {errors.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

Checkbox.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func,
}

export default Checkbox
