import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import classNames from 'classnames'
import { format, isValid, parseISO } from 'date-fns'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import { getDateFormat, getLocale, parseDate } from 'rdmo/core/assets/js/utils/date'

import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'
import { isDefaultValue } from '../../../../../utils/value'

const DateInput = ({ question, value, buttons, disabled, onChange }) => {
  const handleChange = (date) => {
    const text = format(date, 'yyyy-MM-dd')
    onChange(value, { text, unit: question.unit, value_type: question.value_type })
  }

  const handleRawChange = useDebouncedCallback((event) => {
    const date = parseDate(event.target.value)
    if (isValid(date)) {
      handleChange(date)
    }
  }, 500)

  const classnames = classNames({
    'form-control': true,
    'date-control': true,
    'default': isDefaultValue(question, value)
  })

  const getSelected = () => isEmpty(value.text) ? null : parseISO(value.text)

  return (
    <div className="project-interview-input date-input">
      <div className="buttons-wrapper">
        {buttons}
        <DatePicker
          className={classnames}
          selected={getSelected()}
          openToDate={getSelected()}
          onChange={(date) => handleChange(date)}
          onChangeRaw={(event) => handleRawChange(event)}
          locale={getLocale()}
          dateFormat={getDateFormat()}
          disabled={disabled}
          popperPlacement="bottom-start"
          showPopperArrow={false}
          ariaLabelledBy={getQuestionTextId(question)}
          ariaDescribedBy={getQuestionHelpId(question)}
        />
      </div>
    </div>
  )
}

DateInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  buttons: PropTypes.node.isRequired,
  disabled: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default DateInput
