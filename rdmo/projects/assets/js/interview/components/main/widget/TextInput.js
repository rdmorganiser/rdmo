import React, { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'

import { isDefaultValue } from '../../../utils/value'

import useFocusEffect from '../../../hooks/useFocusEffect'

import Unit from './common/Unit'

const TextInput = ({ question, value, disabled, focus, updateValue, buttons }) => {
  const ref = useRef(null)
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {setInputValue(value.text)}, [value.id])
  useFocusEffect(ref, [value.text], focus)

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text })
  }, 500)

  const classnames = classNames({
    'form-control': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input">
      <div className="buttons-wrapper">
        {buttons}
        <input
          ref={ref}
          type="text"
          className={classnames}
          disabled={disabled}
          value={inputValue}
          onChange={(event) => {
            setInputValue(event.target.value)
            handleChange(value, event.target.value)
          }}
        />
      </div>
      <Unit unit={question.unit} />
    </div>
  )
}

TextInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  focus: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default TextInput
