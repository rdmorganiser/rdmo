import React from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil } from 'lodash'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const CheckboxInput = ({ question, value, option, disabled, onCreate, onUpdate, onDelete }) => {

  const checked = !isNil(value)

  const handleCreate = (option, additionalInput) => {
  if (option.has_provider) {
      onCreate([{
        external_id: option.id,
        text: option.text
      }])
    } else {
      onCreate([{
        option: option.id,
        text: additionalInput
      }])
    }
  }

  const handleChange = () => {
    if (checked) {
      onDelete(value)
    } else {
      handleCreate(option)
    }
  }

  const handleAdditionalValueChange = useDebouncedCallback((value, option, additionalInput) => {
    if (checked) {
      if (option.has_provider) {
        onUpdate(value, {
          text: option.text,
          external_id: option.id,
          unit: question.unit,
          value_type: question.value_type
        })
      } else {
        onUpdate(value, {
          text: additionalInput,
          option: option.id,
          unit: question.unit,
          value_type: question.value_type
        })
      }
    } else {
      handleCreate(option, additionalInput)
    }
  }, 500)

  return (
    <div className="checkbox">
      <label>
        <input
          type="checkbox"
          checked={checked}
          disabled={disabled}
          onChange={() => handleChange()}
        />
        <OptionText option={option} />
        {
          isEmpty(option.additional_input) && (
            <OptionHelp className="ml-10" option={option} />
          )
        }
        {
          option.additional_input == 'text' && (
            <>
              <span>:</span>
              <AdditionalTextInput className="ml-10" value={value} option={option} disabled={disabled} onChange={handleAdditionalValueChange} />
              <OptionHelp className="ml-10" option={option} />
            </>
          )
        }
        {
          option.additional_input == 'textarea' && (
            <>
              <span>:</span>
              <AdditionalTextareaInput value={value} option={option} disabled={disabled} onChange={handleAdditionalValueChange} />
              <div>
                <OptionHelp option={option} />
              </div>
            </>
          )
        }
      </label>
    </div>
  )
}

CheckboxInput.propTypes = {
  question: PropTypes.object,
  value: PropTypes.object,
  option: PropTypes.object,
  disabled: PropTypes.bool,
  onCreate: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default CheckboxInput
