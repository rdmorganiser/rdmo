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

const Number = ({ element, field, onChange }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field),
    label = getLabel(element, field, meta),
    help = getHelp(element, field, meta),
    errors = get(element, ['errors', field])

  const className = classNames('form-control', {
    'is-invalid': !isEmpty(errors)
  })

  const value = isNil(element[field]) ? '' : element[field]

  return (
    <div className="mb-3">
      <label className="form-label" htmlFor={id}>{label}</label>
      <input type="number" id={id} className={className} disabled={element.read_only}
        value={value} onChange={event => onChange(field, event.target.value)} />

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

Number.propTypes = {
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default Number
