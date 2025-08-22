import React, { useRef } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil } from 'lodash'

import useAdditionalInputs from '../../../hooks/useAdditionalInputs'
import useAdjustLabel from '../../../hooks/useAdjustLabel'
import useIdle from '../../../hooks/useIdle'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const CheckboxInput = ({ question, value, option, optionIndex, disabled, onCreate, onUpdate, onDelete }) => {

  const ref = useRef(null)
  const [getAdditionalInput, setAdditionalInput] = useAdditionalInputs(value, [option])
  const [idle, setIdle] = useIdle([value])

  useAdjustLabel(ref)

  const checked = !isNil(value)

  const classnames = classNames('checkbox', {
    'text-muted': disabled
  })

  const handleCreate = (option, optionIndex, additionalInput) => {
  if (option.has_provider) {
      onCreate([{
        external_id: option.id,
        text: option.text,
        collection_index: optionIndex
      }])
    } else {
      onCreate([{
        option: option.id,
        text: additionalInput || option.default_text || '',
        collection_index: optionIndex
      }])
    }
  }

  const handleChange = () => {
    if (idle) {
      setIdle(false)
      handleAdditionalInputChange.cancel()

      if (checked) {
        onDelete(value)
        setAdditionalInput(option, '')
      } else {
        handleCreate(option, optionIndex, getAdditionalInput(option))
      }
    }
  }

  const handleAdditionalInputChange = useDebouncedCallback((value, option, additionalInput) => {
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
      handleCreate(option, optionIndex, additionalInput)
    }
  }, 500)

  return (
    <div ref={ref} className={classnames}>
      <label>
        <input
          type="checkbox"
          checked={checked}
          disabled={disabled}
          aria-label={option.text}
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
              <AdditionalTextInput
                className="ml-10"
                inputValue={getAdditionalInput(option)}
                disabled={disabled}
                onChange={(additionalInput) => {
                  setAdditionalInput(option, additionalInput)
                  handleAdditionalInputChange(value, option, additionalInput)
                }}
              />
              <OptionHelp className="ml-10" option={option} />
            </>
          )
        }
        {
          option.additional_input == 'textarea' && (
            <>
              <span>:</span>
              <AdditionalTextareaInput
                inputValue={getAdditionalInput(option)}
                disabled={disabled}
                onChange={(additionalInput) => {
                  setAdditionalInput(option, additionalInput)
                  handleAdditionalInputChange(value, option, additionalInput)
                }}
              />
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
  optionIndex: PropTypes.number,
  disabled: PropTypes.bool,
  onCreate: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default CheckboxInput
