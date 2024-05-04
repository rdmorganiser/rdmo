import React from 'react'
import PropTypes from 'prop-types'

import { checkQuestion } from '../../../utils/page'

import QuestionAddValueHelp from './QuestionAddValueHelp'
import QuestionHelp from './QuestionHelp'
import QuestionManagement from './QuestionManagement'
import QuestionOptional from './QuestionOptional'
import QuestionText from './QuestionText'
import QuestionWarning from './QuestionWarning'
import QuestionWidget from './QuestionWidget'

const Question = ({ templates, question, values, disabled, isManager, focus,
                    currentSet, createValue, updateValue, deleteValue }) => {
  return checkQuestion(question, currentSet) && (
    <div className={`interview-question col-md-${question.width || '12'}`}>
      <QuestionOptional question={question} />
      <QuestionText question={question} />
      <QuestionHelp question={question} />
      <QuestionAddValueHelp templates={templates} question={question} />
      <QuestionWarning templates={templates} question={question} values={values} />
      <QuestionManagement question={question} isManager={isManager} />
      <QuestionWidget
        question={question}
        values={values}
        disabled={disabled}
        focus={focus}
        currentSet={currentSet}
        createValue={createValue}
        updateValue={updateValue}
        deleteValue={deleteValue}
      />
    </div>
  )
}

Question.propTypes = {
  templates: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool.isRequired,
  isManager: PropTypes.bool.isRequired,
  focus: PropTypes.bool.isRequired,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
}

export default Question
