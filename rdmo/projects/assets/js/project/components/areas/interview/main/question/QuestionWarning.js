import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionWarning = ({ question, values }) => {
  return !question.is_collection && values.length > 1 && (
    <Template template="project_interview_multiple_values_warning" />
  )
}

QuestionWarning.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired
}

export default QuestionWarning
