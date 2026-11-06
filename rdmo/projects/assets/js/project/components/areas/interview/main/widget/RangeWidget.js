import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionCopyValue from '../question/QuestionCopyValue'
import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionDefault from '../question/QuestionDefault'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'
import QuestionReuseValue from '../question/QuestionReuseValue'
import QuestionSuccess from '../question/QuestionSuccess'

import RangeInput from './RangeInput'

const RangeWidget = ({ question, sets, values, siblings, currentSet }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()

  return (
    <div className="project-interview-widgets">
      <div className="d-flex flex-column justify-content-between gap-2">
        {
          values.map((value, valueIndex) => {
            return (
              <div key={valueIndex} className="project-interview-widget">
                <RangeInput
                  question={question}
                  value={value}
                  disabled={readOnly}
                  onChange={(value, attr) => dispatch(updateValue(value, attr))}
                  buttons={
                    (
                      <div className="buttons">
                        <QuestionSuccess value={value}/>
                        <QuestionReuseValue question={question} value={value} />
                        <QuestionCopyValue question={question} value={value} siblings={siblings} />
                        <QuestionEraseValue question={question} value={value} />
                        <QuestionRemoveValue question={question} values={values} value={value} />
                        <QuestionDefault question={question} value={value} />
                      </div>
                    )
                  }
                />
                <QuestionError value={value} />
              </div>
            )
          })
        }
        <div className="buttons">
          <QuestionAddValue
            question={question}
            values={values}
            currentSet={currentSet}
          />
          <QuestionCopyValues
            question={question}
            sets={sets}
            values={values}
            siblings={siblings}
            currentSet={currentSet}
          />
        </div>
      </div>
    </div>
  )
}

RangeWidget.propTypes = {
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  currentSet: PropTypes.object.isRequired,
}

export default RangeWidget
