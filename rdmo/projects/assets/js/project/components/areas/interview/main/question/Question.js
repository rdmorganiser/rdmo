import React from 'react'
import PropTypes from 'prop-types'

import { useQuestionHelp } from '../../../../../hooks'
import { checkQuestion } from '../../../../../utils/page'
import { getQuestionHelpId } from '../../../../../utils/question'

import QuestionAddValueHelp from './QuestionAddValueHelp'
import QuestionContact from './QuestionContact'
import QuestionHelp from './QuestionHelp'
import QuestionHelpTemplate from './QuestionHelpTemplate'
import QuestionHelpToggle from './QuestionHelpToggle'
import QuestionManagement from './QuestionManagement'
import QuestionOptional from './QuestionOptional'
import QuestionText from './QuestionText'
import QuestionWarning from './QuestionWarning'
import QuestionWidget from './QuestionWidget'

const Question = ({ question, sets, values, siblings, currentSet }) => {
  const [showHelp, toggleHelp] = useQuestionHelp(question)

  return checkQuestion(question, currentSet) && (
    <div className={`project-interview-question col-md-${question.width || '12'}`}>
      <div className="project-interview-question-text">
        <div className="d-flex gap-2 mb-3">
          <QuestionText question={question} currentSet={currentSet} />
          <QuestionContact question={question} values={values} />
          <div className="ms-auto"></div>
          <QuestionOptional question={question} />
          <QuestionHelpToggle question={question} currentSet={currentSet} show={showHelp} onClick={toggleHelp} />
        </div>
      </div>
      <div id={getQuestionHelpId(question, currentSet)}>
        <QuestionHelp question={question} show={showHelp} />
        <QuestionHelpTemplate show={showHelp} />
        <QuestionAddValueHelp question={question} show={showHelp} />
      </div>
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
