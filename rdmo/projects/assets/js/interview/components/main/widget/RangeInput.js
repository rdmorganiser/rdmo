import React, { useEffect, useLayoutEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import classNames from 'classnames'
import { isNil, toString } from 'lodash'

import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
import { isDefaultValue } from '../../../utils/value'

import Unit from './common/Unit'

const RangeInput = ({ question, value, disabled, updateValue, buttons }) => {
  const ref = useRef(null)
  const [inputValue, setInputValue] = useState('')

  useEffect(() => setInputValue(value.text), [value.text])

  useLayoutEffect(() => {
    if (ref.current) {
      const unitElement = ref.current.nextElementSibling

      // Setup canvas for text measurement
      const canvas = document.createElement('canvas')
      const context = canvas.getContext('2d')
      context.font = window.getComputedStyle(ref.current).font || '14px Arial'

      let numberWidth
      if (isNil(question.maximum)) {
        numberWidth = 30 // fallback width for unknown max
      } else {
        const step = isNil(question.step) ? 1 : question.step
        const decimals = toString(step).split('.')[1]?.length || 0
        const maxString = toString(question.maximum.toFixed(decimals))
        numberWidth = context.measureText(maxString).width
      }

      const unitWidth = context.measureText(question.unit ?? '').width
      const totalWidth = Math.ceil(numberWidth + unitWidth + 8) // buffer

      unitElement.style.flex = `0 0 ${totalWidth}px`
    }
  }, [question])

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text, unit: question.unit, value_type: question.value_type })
  }, 500)

  const classnames = classNames({
    'interview-input': true,
    'range-input': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className={classnames}>
      <input
        ref={ref}
        type="range"
        min={isNil(question.minimum) ? '0' : question.minimum}
        max={isNil(question.maximum) ? '100' : question.maximum}
        step={isNil(question.step) ? '1' : question.step}
        aria-labelledby={getQuestionTextId(question)}
        aria-describedby={getQuestionHelpId(question)}
        disabled={disabled}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value)
          handleChange(value, event.target.value)
        }}
      />
      <Unit unit={question.unit} inputValue={inputValue} />
      {buttons}
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
