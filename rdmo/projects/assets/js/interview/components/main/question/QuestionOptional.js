import React from 'react'
import PropTypes from 'prop-types'

const QuestionOptional = ({ question }) => {
  return question.is_optional && (
    <div className="badge badge-optional" title={gettext('This is an optional question.')}>
      {gettext('Optional')}
    </div>
  )
}

QuestionOptional.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionOptional
