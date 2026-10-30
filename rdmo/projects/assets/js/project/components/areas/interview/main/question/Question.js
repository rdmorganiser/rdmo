import React from 'react'
import PropTypes from 'prop-types'

import { checkQuestion } from '../../../../../utils/page'

import QuestionAddValueHelp from './QuestionAddValueHelp'
import QuestionContact from './QuestionContact'
import QuestionHelp from './QuestionHelp'
import QuestionHelpTemplate from './QuestionHelpTemplate'
import QuestionManagement from './QuestionManagement'
import QuestionOptional from './QuestionOptional'
import QuestionText from './QuestionText'
import QuestionWarning from './QuestionWarning'
import QuestionWidget from './QuestionWidget'

const Question = ({ question, sets, values, siblings, currentSet }) => {
  return checkQuestion(question, currentSet) && (
    <div className={`project-interview-question col-md-${question.width || '12'}`}>
      <div className="project-interview-question-text">
        <div className="d-flex gap-2 mb-3">
          <QuestionText question={question} />
          <QuestionContact question={question} values={values} />
          <div className="ms-auto"></div>
          <QuestionOptional question={question} />
        </div>
      </div>
      <QuestionHelp question={question} />
      <QuestionHelpTemplate />
      <QuestionAddValueHelp question={question} />
      <QuestionWarning question={question} values={values} />
      <QuestionManagement question={question} />
      <QuestionWidget
        question={question}
        sets={sets}
        values={values}
        siblings={siblings}
        currentSet={currentSet}
      />
    </div>
  )
}

Question.propTypes = {
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  currentSet: PropTypes.object.isRequired,
}

export default Question
