import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionWarning = ({ templates, question, values }) => {
  return !question.is_collection && values.length > 1 && (
    <Html html={templates.project_interview_multiple_values_warning} />
  )
}

QuestionWarning.propTypes = {
  templates: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired
}

export default QuestionWarning
