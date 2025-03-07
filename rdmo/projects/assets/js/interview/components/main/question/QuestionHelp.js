import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { getQuestionHelpId } from '../../../utils/question'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionHelp = ({ question }) => {
  const classnames = classNames('interview-question-help', {
    'text-muted': question.is_optional
  })

  return <div className={classnames} >
    <Html id={getQuestionHelpId(question)} html={question.help} />
  </div>
}

QuestionHelp.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionHelp
