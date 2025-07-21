import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { getQuestionTextId } from '../../../utils/question'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionText = ({ question }) => {
  const classnames = classNames({
    'form-label': true,
    'text-muted': question.is_optional
  })

  return (
    <div className={classnames}>
      <Html id={getQuestionTextId(question)} html={question.text} />
    </div>
  )
}

QuestionText.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionText
