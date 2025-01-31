import React from 'react'
import PropTypes from 'prop-types'
import { maxBy } from 'lodash'

import { gatherOptions } from '../../../utils/options'

import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionEraseValues from '../question/QuestionEraseValues'
import QuestionError from '../question/QuestionError'
import QuestionReuseValues from '../question/QuestionReuseValues'
import QuestionSuccess from '../question/QuestionSuccess'

import CheckboxInput from './CheckboxInput'

const CheckboxWidget = ({ page, question, sets, values, siblings, currentSet, disabled,
                          createValue, updateValue, deleteValue, copyValue }) => {

  const handleCreateValue = (attrsList) => {
    const lastValue = maxBy(values, (v) => v.collection_index)

    let collectionIndex = lastValue ? lastValue.collection_index + 1 : 0
    attrsList.forEach(attrs => {
      createValue({
        attribute: question.attribute,
        set_prefix: currentSet.set_prefix,
        set_index: currentSet.set_index,
        collection_index: collectionIndex,
        set_collection: question.set_collection,
        unit: question.unit,
        value_type: question.value_type,
        ...attrs
      }, true)
      collectionIndex += 1
    })
  }

  const success = values.some((value) => value.success)

  return (
    <div className="interview-widgets">
      <div className="interview-widget">
        <div className="interview-input">
          <div className="buttons-wrapper">
            <div className="checkbox-control">
              {
                gatherOptions(question).map((option, optionIndex) => {
                  const value = values.find((value) => (
                    option.has_provider ? (value.external_id === option.id) : (value.option === option.id)
                  ))

                  return (
                    <React.Fragment key={optionIndex}>
                      <CheckboxInput
                        question={question}
                        value={value}
                        option={option}
                        disabled={disabled}
                        onCreate={handleCreateValue}
                        onUpdate={updateValue}
                        onDelete={deleteValue}
                      />
                      <QuestionError value={value} />
                    </React.Fragment>
                  )
                })
              }
            </div>
            <div className="buttons">
              <QuestionSuccess value={{ success }} />
              <QuestionEraseValues
                values={values}
                disabled={disabled}
                deleteValue={deleteValue}
              />
              <QuestionReuseValues
                page={page}
                question={question}
                values={values}
                createValues={handleCreateValue}
                updateValue={updateValue}
                deleteValue={deleteValue}
              />
              <QuestionCopyValues
                question={question}
                sets={sets}
                values={values}
                siblings={siblings}
                currentSet={currentSet}
                copyValue={copyValue}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

CheckboxWidget.propTypes = {
  page: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default CheckboxWidget
