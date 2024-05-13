import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const QuestionText = ({ question }) => {
  const classnames = classNames({
    'form-label': true,
    'text-muted': question.is_optional
  })

  return (
    <div className={classnames}>
      {question.text}
    </div>
  )
}

QuestionText.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionText