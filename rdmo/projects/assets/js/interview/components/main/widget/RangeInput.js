import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { isDefaultValue } from '../../../utils/value'

import Unit from './common/Unit'

const RangeInput = ({ question, value, disabled, updateValue, buttons }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.text])

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text })
  }, 500)

  const classnames = classNames({
    'interview-input': true,
    'range': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className={classnames}>
      <input
        type="range"
        min={isEmpty(question.minimum) ? '0' : question.minimum}
        max={isEmpty(question.maximum) ? '100' : question.maximum}
        step={isEmpty(question.step) ? '1' : question.step}
        disabled={disabled}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value)
          handleChange(value, event.target.value)
        }}
      />
      {buttons}
      <Unit unit={question.unit} inputValue={inputValue} />
    </div>
  )
}

RangeInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default RangeInput
