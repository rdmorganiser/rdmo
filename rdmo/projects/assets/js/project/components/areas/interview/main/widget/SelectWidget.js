import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { gatherOptions } from '../../../../../utils/options'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionCopyValue from '../question/QuestionCopyValue'
import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionDefault from '../question/QuestionDefault'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'
import QuestionReuseValue from '../question/QuestionReuseValue'
import QuestionSuccess from '../question/QuestionSuccess'

import SelectInput from './SelectInput'

const SelectWidget = ({ question, sets, values, siblings, creatable, currentSet }) => {
  const dispatch = useDispatch()
  const providerOptions = useSelector((state) => state.interview.providerOptions)
  const readOnly = useReadOnly()

  return (
    <div className="project-interview-widgets">
      <div className="d-flex flex-column justify-content-between gap-2">
        {
          values.map((value, valueIndex) => {
            return (
              <div key={valueIndex} className="project-interview-widget">
                <SelectInput
                  question={question}
                  value={value}
                  options={gatherOptions(question, currentSet, providerOptions)}
                  creatable={creatable}
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

SelectWidget.propTypes = {
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  creatable: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
}

export default SelectWidget
