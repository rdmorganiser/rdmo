import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const Checkbox = ({ element, field, onChange }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field),
        label = getLabel(element, field, meta),
        help = getHelp(element, field, meta),
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
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func,
}

export default Checkbox
