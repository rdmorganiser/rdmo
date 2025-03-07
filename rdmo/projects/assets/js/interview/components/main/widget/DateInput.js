import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import classNames from 'classnames'
import { enGB, de, it, es, fr } from 'date-fns/locale'

import lang from 'rdmo/core/assets/js/utils/lang'

import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
import { isDefaultValue } from '../../../utils/value'

const DateInput = ({ question, value, disabled, updateValue, buttons }) => {

  const getLocale = () => {
    switch (lang) {
      case 'de':
        return de
      case 'it':
        return it
      case 'es':
        return es
      case 'fr':
        return fr
      default:
        return enGB
    }
  }

  const getDateFormat = () => {
    switch (lang) {
      case 'de':
        return 'dd.MM.yyyy'
      case 'it':
        return 'dd/MM/yyyy'
      case 'es':
        return 'dd/MM/yyyy'
      case 'fr':
        return 'dd/MM/yyyy'
      default:
        return 'dd/MM/yyyy'
    }
  }

  const handleChange = (date) => {
    const text = date.toISOString().slice(0,10)
    updateValue(value, { text, unit: question.unit, value_type: question.value_type })
  }

  const classnames = classNames({
    'form-control': true,
    'date-control': true,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input date-input">
      <div className="buttons-wrapper">
        {buttons}
        <DatePicker
          className={classnames}
          selected={value.text}
          onChange={(date) => handleChange(date)}
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
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default DateInput
