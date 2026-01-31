import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const Textarea = ({ element, field, rows, onChange }) => {
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
      <textarea id={id} className={className} rows={rows} disabled={element.read_only}
                value={value} onChange={event => onChange(field, event.target.value)}  />
      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

Textarea.propTypes = {
  element: PropTypes.object,
  field: PropTypes.string,
  rows: PropTypes.number,
  onChange: PropTypes.func
}

export default Textarea
