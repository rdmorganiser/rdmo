import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'
import ReactCodeMirror from '@uiw/react-codemirror'
import { json } from '@codemirror/lang-json'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const JsonField = ({ config, element, field, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warnings = get(element, ['warnings', field]),
        errors = get(element, ['errors', field])

  const [value, setValue] = useState(formatValue(element[field]))
  const [parseError, setParseError] = useState(false)

  useEffect(() => {
    setValue(formatValue(element[field]))
  }, [element, field])

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warnings) || parseError,
    'has-error': !isEmpty(errors)
  })

  const handleChange = (newValue) => {
    setValue(newValue)
    try {
      const parsed = newValue.trim() ? JSON.parse(newValue) : {}
      setParseError(false)
      onChange(field, parsed)
    } catch (e) {
      setParseError(true)
    }
  }

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactCodeMirror className="codemirror form-control" id={id} value={value}
                       extensions={[json()]}
                       onChange={handleChange} disabled={element.read_only} />

      {help && <p className="help-block">{help}</p>}
      {parseError && <p className="help-block text-warning">{gettext('Please provide valid JSON.')}</p>}

      {errors && <ul className="help-block list-unstyled">
        {errors.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

const formatValue = (value) => {
  if (isNil(value)) return ''
  if (typeof value === 'string') return value
  try {
    return JSON.stringify(value, null, 2)
  } catch (e) {
    return ''
  }
}

JsonField.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  onChange: PropTypes.func
}

export default JsonField
