import React, { useState, useEffect, useLayoutEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'

import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
import { isDefaultValue } from '../../../utils/value'

import useFocusEffect from '../../../hooks/useFocusEffect'

import Unit from './common/Unit'

const TextInput = ({ question, value, disabled, updateValue, buttons }) => {
  const ref = useRef(null)
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {setInputValue(value.text)}, [value.text])
  useFocusEffect(ref, value.focus)
  useLayoutEffect(() => {
    if (ref.current) {
      // add a right padding of the size of the buttons div, plus some space for the success indicator
      const buttonsWidth = ref.current.previousElementSibling.offsetWidth + 20
      ref.current.style.paddingRight = `${buttonsWidth}px`
    }
  }, [buttons])

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text, unit: question.unit, value_type: question.value_type })
  }, 500)

  const classnames = classNames({
    'form-control': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input text-input">
      <div className="buttons-wrapper">
        {buttons}
        <input
          ref={ref}
          type="text"
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
      </div>
      <Unit unit={question.unit} />
    </div>
  )
}

TextInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default TextInput
