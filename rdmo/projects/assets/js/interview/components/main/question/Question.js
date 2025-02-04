import React from 'react'
import PropTypes from 'prop-types'

import { checkQuestion } from '../../../utils/page'

import QuestionAddValueHelp from './QuestionAddValueHelp'
import QuestionContact from './QuestionContact'
import QuestionHelp from './QuestionHelp'
import QuestionHelpTemplate from './QuestionHelpTemplate'
import QuestionManagement from './QuestionManagement'
import QuestionOptional from './QuestionOptional'
import QuestionText from './QuestionText'
import QuestionWarning from './QuestionWarning'
import QuestionWidget from './QuestionWidget'

const Question = ({ settings, templates, page, question, sets, values, siblings, disabled, isManager,
                    currentSet, createValue, updateValue, deleteValue, copyValue, fetchContact }) => {
  return checkQuestion(question, currentSet) && (
    <div className={`interview-question col-md-${question.width || '12'}`}>
      <QuestionOptional question={question} />
      <div className="interview-question-text">
        <QuestionText question={question} />
        <QuestionContact settings={settings} question={question} values={values} fetchContact={fetchContact} />
      </div>
      <QuestionHelp question={question} />
      <QuestionHelpTemplate templates={templates} />
      <QuestionAddValueHelp templates={templates} question={question} disabled={disabled} />
      <QuestionWarning templates={templates} question={question} values={values} />
      <QuestionManagement question={question} isManager={isManager} />
      <QuestionWidget
        page={page}
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
  settings: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
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
  copyValue: PropTypes.func.isRequired,
  fetchContact: PropTypes.func.isRequired
}

export default Question
