import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionHelp = ({ question, show }) => {
  const classnames = classNames('project-interview-question-help font-small text-muted mb-2', {
    'd-none': !show
  })

  return (
    <div className={classnames} >
      <Html html={question.help} />
    </div>
  )
}

QuestionHelp.propTypes = {
  question: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired
}

export default QuestionHelp
