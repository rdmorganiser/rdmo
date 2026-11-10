import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

import { getQuestionTextId } from '../../../../../utils/question'

const QuestionText = ({ question, currentSet }) => {
  const classnames = classNames('mb-0', {
    'text-muted': question.is_optional
  })

  return (
    <h3 className={classnames}>
      <Html id={getQuestionTextId(question, currentSet)} html={question.text} />
    </h3>
  )
}

QuestionText.propTypes = {
  question: PropTypes.object.isRequired,
  currentSet: PropTypes.object.isRequired
}

export default QuestionText
