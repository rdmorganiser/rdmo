import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { createValue, deleteValue, updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { gatherOptions } from '../../../../../utils/options'
import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'

import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionEraseValues from '../question/QuestionEraseValues'
import QuestionError from '../question/QuestionError'
import QuestionReuseValues from '../question/QuestionReuseValues'
import QuestionSuccess from '../question/QuestionSuccess'

import CheckboxInput from './CheckboxInput'

const CheckboxWidget = ({ question, sets, values, siblings, currentSet }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()

  const handleCreate = (attrsList) => {
    attrsList.forEach(attrs => {
      dispatch(createValue({
        attribute: question.attribute,
        set_prefix: currentSet.set_prefix,
        set_index: currentSet.set_index,
        set_collection: question.set_collection,
        unit: question.unit,
        value_type: question.value_type,
        ...attrs
      }, true))
    })
  }

  const handleUpdate = (value, attrs) => dispatch(updateValue(value, attrs))

  const handleDelete = (value) => dispatch(deleteValue(value))

  const success = values.some((value) => value.success)

  return (
    <div className="project-interview-widgets">
      <div className="project-interview-widget">
        <div className="project-interview-input checkbox-input">
          <div className="buttons-wrapper">
            <fieldset
              aria-labelledby={getQuestionTextId(question)}
              aria-describedby={getQuestionHelpId(question)}
            >
              <div className="d-flex flex-column align-items-top gap-2">
                {
                  gatherOptions(question, currentSet).map((option, optionIndex) => {
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
                          disabled={readOnly}
                          onCreate={handleCreate}
                          onUpdate={handleUpdate}
                          onDelete={handleDelete}
                        />
                        <QuestionError value={value} />
                      </React.Fragment>
                    )
                  })
                }
              </div>
            </fieldset>
            <div className="buttons">
              <QuestionSuccess value={{ success }} />
              <QuestionReuseValues
                question={question}
                values={values}
                onCreate={handleCreate}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
              />
              <QuestionCopyValues
                question={question}
                sets={sets}
                values={values}
                siblings={siblings}
                currentSet={currentSet}
              />
              <QuestionEraseValues values={values} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

CheckboxWidget.propTypes = {
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
}

export default CheckboxWidget
