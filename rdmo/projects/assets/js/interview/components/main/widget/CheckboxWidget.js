import React from 'react'
import PropTypes from 'prop-types'


import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
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
    attrsList.forEach(attrs => {
      createValue({
        attribute: question.attribute,
        set_prefix: currentSet.set_prefix,
        set_index: currentSet.set_index,
        set_collection: question.set_collection,
        unit: question.unit,
        value_type: question.value_type,
        ...attrs
      }, true)
    })
  }

  const success = values.some((value) => value.success)

  return (
    <div className="interview-widgets">
      <div className="interview-widget">
        <div className="interview-input checkbox-input">
          <div className="buttons-wrapper">
            <fieldset className="checkbox-control"
                      aria-labelledby={getQuestionTextId(question)}
                      aria-describedby={getQuestionHelpId(question)}>
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
                        optionIndex={optionIndex}
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
            </fieldset>
            <div className="buttons">
              <QuestionSuccess value={{ success }} />
              <QuestionReuseValues
                page={page}
                question={question}
                values={values}
                disabled={disabled}
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
              <QuestionEraseValues
                values={values}
                disabled={disabled}
                deleteValue={deleteValue}
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
