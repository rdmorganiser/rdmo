import React from 'react'
import PropTypes from 'prop-types'
import DatePicker from 'react-datepicker'
import { enGB, de, it, es, fr } from 'date-fns/locale'

import lang from 'rdmo/core/assets/js/utils/lang'

import AddValue from './common/AddValue'
import RemoveValue from './common/RemoveValue'

const DateInput = ({ value, disabled, updateValue }) => {

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

  return (
    <DatePicker
      className="form-control date-control"
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
  updateValue: PropTypes.func.isRequired
}

const DateWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => (
          <div key={valueIndex} className="interview-input">
            <div className="interview-input-options">
              {
                question.is_collection && <RemoveValue value={value} deleteValue={deleteValue} />
              }
            </div>
            <DateInput
              value={value}
              disabled={disabled}
              updateValue={updateValue}
            />
          </div>
        ))
      }
      {
        question.is_collection && (
          <AddValue question={question} values={values} currentSet={currentSet} createValue={createValue} />
        )
      }
    </div>
  )
}

DateWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default DateWidget
