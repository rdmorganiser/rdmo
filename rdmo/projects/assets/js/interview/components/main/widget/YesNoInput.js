import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { isDefaultValue } from '../../../utils/value'

import Unit from './common/Unit'

const YesNoInput = ({ question, value, disabled, updateValue, buttons }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id, value.text])

  const handleChange = (value, text) => {
    updateValue(value, { text, unit: question.unit, value_type: question.value_type })
  }

  const classnames = classNames({
    'radio-control': true,
    'radio': true,
    'yesno': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input yesno-input">
      <div className="buttons-wrapper">
        {buttons}
        <div className={classnames}>
          <label>
              <input
                type="radio"
                value="1"
                disabled={disabled}
                checked={inputValue == '1'}
                onChange={(event) => {
                  setInputValue(event.target.value)
                  handleChange(value, event.target.value)
                }} />
              <span>{gettext('Yes')}</span>
          </label>
          <label>
              <input
                type="radio"
                value="0"
                checked={inputValue == '0'}
                disabled={disabled}
                onChange={(event) => {
                  setInputValue(event.target.value)
                  handleChange(value, event.target.value)
                }} />
              <span>{gettext('No')}</span>
          </label>
        </div>
      </div>
      <Unit question={question} />
    </div>
  )
}

YesNoInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default YesNoInput
