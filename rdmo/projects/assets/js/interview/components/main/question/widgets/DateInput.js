import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import classNames from 'classnames'
import { enGB, de, it, es, fr } from 'date-fns/locale'

import lang from 'rdmo/core/assets/js/utils/lang'

const DateInput = ({ value, disabled, isDefault, updateValue }) => {

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
    updateValue(value, { text })
  }

  const classnames = classNames({
    'form-control': true,
    'date-control': true,
    'default': isDefault
  })

  return (
    <DatePicker
      className={classnames}
      selected={value.text}
      onChange={(date) => handleChange(date)}
      locale={getLocale()}
      dateFormat={getDateFormat()}
      disabled={disabled}
    />
  )
}

DateInput.propTypes = {
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default DateInput
