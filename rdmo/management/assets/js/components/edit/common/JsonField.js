import React, { forwardRef, useEffect, useImperativeHandle, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'
import ReactCodeMirror from '@uiw/react-codemirror'
import { json } from '@codemirror/lang-json'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const JsonField = forwardRef(({ config, element, field, disabled = false }, ref) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warnings = get(element, ['warnings', field]),
        errors = get(element, ['errors', field])

  const [value, setValue] = useState(formatValue(element[field]))
  const [parseError, setParseError] = useState(null)

  useEffect(() => {
    setValue(formatValue(element[field]))
  }, [element.id, field])

  useImperativeHandle(ref, () => ({
    commit: () => {
      try {
        const parsed = value.trim() ? JSON.parse(value) : {}
        setParseError(null)
        return parsed
      } catch (e) {
        setParseError(getParseErrorMessageFromError(e))
        return undefined
      }
    }
  }), [value])

  const className = classNames({
    'form-group': true,
    'is-disabled': disabled || element.read_only,
    'has-warning': !isEmpty(warnings) || parseError,
    'has-error': !isEmpty(errors)
  })

  const handleChange = (newValue) => {
    if (disabled || element.read_only) {
      return
    }
    setValue(newValue)
    setParseError(validateJson(newValue))
  }

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactCodeMirror
        className={classNames('codemirror form-control', { 'is-disabled': disabled })}
        id={id}
        value={value}
        extensions={[json()]}
        onChange={handleChange}
        editable={!(element.read_only || disabled)}
      />

      {help && <p className="help-block">{help}</p>}
      {parseError && (
        <>
          <p className="help-block text-warning">
            {parseError}
          </p>
          <p className="help-block">
            {gettext('Example:')} <code>{'{ "key1": "value", "key2": "value" }'}</code>
          </p>
        </>
      )}

      {errors && (
        <ul className="help-block list-unstyled">
          {errors.map((error, index) => (
            <li key={index}>{error}</li>
          ))}
        </ul>
      )}
    </div>
  )
})

JsonField.displayName = 'JsonField'

const formatValue = (value) => {
  if (isNil(value)) return ''
  if (typeof value === 'string') return value
  try {
    return JSON.stringify(value, null, 2)
  } catch (e) {
    return ''
  }
}

const validateJson = (value) => {
  try {
    JSON.parse(value.trim() ? value : '{}')
    return null
  } catch (e) {
    return getParseErrorMessageFromError(e)
  }
}

const getParseErrorMessageFromError = (error) => {
  if (error instanceof SyntaxError && error.message) {
    return error.message
  }
  return gettext('Please provide valid JSON.')
}

JsonField.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  disabled: PropTypes.bool
}

export default JsonField
