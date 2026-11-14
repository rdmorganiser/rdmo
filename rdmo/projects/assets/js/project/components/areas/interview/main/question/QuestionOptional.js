import React from 'react'
import PropTypes from 'prop-types'

const QuestionOptional = ({ question }) => {
  return question.is_optional && (
    <div title={gettext('This is an optional question.')}>
      <code className="code-optional">{gettext('Optional')}</code>
    </div>
  )
}

QuestionOptional.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionOptional
