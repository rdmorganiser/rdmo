import React from 'react'
import PropTypes from 'prop-types'
import { isNil, maxBy } from 'lodash'

import CheckboxInput from './CheckboxInput'

const CheckboxWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {

  const handleCreateValue = (option, text) => {
    const lastValue = maxBy(values, (v) => v.collection_index)
    const collectionIndex = lastValue ? lastValue.collection_index + 1 : 0

    createValue({
      attribute: question.attribute,
      set_prefix: currentSet.set_prefix,
      set_index: currentSet.set_index,
      collection_index: collectionIndex,
      option: option.id,
      text: isNil(text) ? '' : text
    }, true)
  }

  return (
    <div className="interview-collection">
      <div className="interview-input">
        <div className="checkbox-control">
          {
            question.options.map((option, optionIndex) => (
              <CheckboxInput
                key={optionIndex}
                value={values.find((value) => value.option == option.id)}
                option={option}
                disabled={disabled}
                onCreate={handleCreateValue}
                onUpdate={updateValue}
                onDelete={deleteValue}
              />
            ))
          }
        </div>
      </div>
    </div>
  )
}

CheckboxWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default CheckboxWidget
