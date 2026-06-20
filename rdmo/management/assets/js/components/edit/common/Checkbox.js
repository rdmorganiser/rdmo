import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import classNames from 'classnames'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getHelp, getId, getLabel } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const Checkbox = ({ element, field, onChange }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field)
  const label = getLabel(element, field, meta)
  const help = getHelp(element, field, meta)
  const errors = get(element, ['errors', field])

  const checked = isNil(element[field]) ? '' : element[field]

  return (
    <div className="mb-3">
      <div className="form-check">
        <input
          type="checkbox"  id={id} disabled={element.read_only}
          className={classNames('form-check-input', {'is-invalid': !isEmpty(errors)})}
          checked={checked} onChange={() => onChange(field, !checked)} />
        <label className="form-check-label" htmlFor={id}>{label}</label>

        <ErrorList errors={errors} />
        <HelpText help={help} />
      </div>
    </div>
  )
}

Checkbox.propTypes = {
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func,
}

export default Checkbox
