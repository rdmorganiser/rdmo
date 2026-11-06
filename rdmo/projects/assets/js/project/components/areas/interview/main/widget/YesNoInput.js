import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'
import { isDefaultValue } from '../../../../../utils/value'

import Unit from './common/Unit'

const YesNoInput = ({ question, value, buttons, disabled, onChange }) => {
  const yesId = `radio-${value.tmp_id || value.id}-yes`
  const noId = `radio-${value.tmp_id || value.id}-no`

  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id, value.text])

  const handleChange = (value, text) => {
    onChange(value, { text, unit: question.unit, value_type: question.value_type })
  }

  const classnames = classNames('radio-control radio yesno', {
    'text-muted': disabled,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="project-interview-input yesno-input">
      <div className="buttons-wrapper">
        {buttons}
        <fieldset
          className={classnames}
          aria-labelledby={getQuestionTextId(question)}
          aria-describedby={getQuestionHelpId(question)}>
          <div className="form-check form-check-inline">
            <input
              id={yesId}
              type="radio"
              className="form-check-input"
              value="1"
              disabled={disabled}
              checked={inputValue == '1'}
              onChange={
                (event) => {
                  setInputValue(event.target.value)
                  handleChange(value, event.target.value)
                }
              }
            />
            <label className="form-check-label" htmlFor={yesId}>
              {gettext('Yes')}
            </label>
          </div>
          <div className="form-check form-check-inline">
            <input
              id={noId}
              type="radio"
              className="form-check-input"
              value="0"
              checked={inputValue == '0'}
              disabled={disabled}
              onChange={
                (event) => {
                  setInputValue(event.target.value)
                  handleChange(value, event.target.value)
                }
              }
            />
            <label className="form-check-label" htmlFor={noId}>
              {gettext('No')}
            </label>
          </div>
        </fieldset>
      </div>
      <Unit question={question} />
    </div>
  )
}

YesNoInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  buttons: PropTypes.node.isRequired,
  disabled: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default YesNoInput
