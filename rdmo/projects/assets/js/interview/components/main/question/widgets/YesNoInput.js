import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const YesNoInput = ({ value, disabled, isDefault, updateValue }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id])

  const handleChange = (value, text) => {
    updateValue(value, { text })
  }

  const classnames = classNames({
    'radio-control': true,
    'default': isDefault
  })

  return (
    <div className={classnames}>
      <div className="radio yesno">
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
  )
}

YesNoInput.propTypes = {
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default YesNoInput
