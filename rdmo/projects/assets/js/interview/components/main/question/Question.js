import React from 'react'
import PropTypes from 'prop-types'

import { checkQuestion } from '../../../utils/page'

import QuestionAddValueHelp from './QuestionAddValueHelp'
import QuestionHelp from './QuestionHelp'
import QuestionHelpTemplate from './QuestionHelpTemplate'
import QuestionManagement from './QuestionManagement'
import QuestionOptional from './QuestionOptional'
import QuestionText from './QuestionText'
import QuestionWarning from './QuestionWarning'
import QuestionWidget from './QuestionWidget'

const Question = ({ templates, question, sets, values, siblings, disabled, isManager,
                    currentSet, createValue, updateValue, deleteValue, copyValue }) => {
  return checkQuestion(question, currentSet) && (
    <div className={`interview-question col-md-${question.width || '12'}`}>
      <QuestionOptional question={question} />
      <QuestionText question={question} />
      <QuestionHelp question={question} />
      <QuestionHelpTemplate templates={templates} />
      <QuestionAddValueHelp templates={templates} question={question} />
      <QuestionWarning templates={templates} question={question} values={values} />
      <QuestionManagement question={question} isManager={isManager} />
      <QuestionWidget
        question={question}
        sets={sets}
        values={values}
        siblings={siblings}
        disabled={disabled}
        currentSet={currentSet}
        createValue={createValue}
        updateValue={updateValue}
        deleteValue={deleteValue}
        copyValue={copyValue}
      />
    </div>
  )
}

Question.propTypes = {
  templates: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  disabled: PropTypes.bool.isRequired,
  isManager: PropTypes.bool.isRequired,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default Question
