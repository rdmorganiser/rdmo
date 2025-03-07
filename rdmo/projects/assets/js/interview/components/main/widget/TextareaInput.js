import React, { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'

import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
import { isDefaultValue } from '../../../utils/value'

import useFocusEffect from '../../../hooks/useFocusEffect'

import Unit from './common/Unit'

const TextareaInput = ({ question, value, disabled, updateValue, buttons }) => {
  const ref = useRef(null)
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {setInputValue(value.text)}, [value.text])
  useFocusEffect(ref, value.focus)

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text, unit: question.unit, value_type: question.value_type })
  }, 500)

  const classnames = classNames({
    'form-control': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input textarea-input">
      <div className="buttons-wrapper">
        <textarea
          ref={ref}
          rows={6}
          className={classnames}
          disabled={disabled}
          aria-labelledby={getQuestionTextId(question)}
          aria-describedby={getQuestionHelpId(question)}
          value={inputValue}
          onChange={(event) => {
            setInputValue(event.target.value)
            handleChange(value, event.target.value)
          }}
        />
        {buttons}
      </div>
      <Unit unit={question.unit} />
    </div>
  )
}

TextareaInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default TextareaInput
