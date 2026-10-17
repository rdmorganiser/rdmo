import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'
import QuestionSuccess from '../question/QuestionSuccess'

import FileInput from './FileInput'

const FileWidget = ({ question, values, currentSet }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()

  return (
    <div className="project-interview-widgets">
      <div className="d-flex flex-column justify-content-between gap-2">
        {
          values.map((value, valueIndex) => {
            return (
              <div key={valueIndex} className="project-interview-widget">
                <FileInput
                  question={question}
                  value={value}
                  disabled={readOnly}
                  onChange={(value, attr) => dispatch(updateValue(value, attr))}
                  buttons={
                    (
                      <div className="buttons">
                        <QuestionSuccess value={value}/>
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
        </div>
      </div>
    </div>
  )
}

FileWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired,
}

export default FileWidget
