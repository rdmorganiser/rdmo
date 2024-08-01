import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionAddValueHelp = ({ templates, question }) => {
  return question.is_collection && (
    <Html html={templates.project_interview_add_value_help} />
  )
}

QuestionAddValueHelp.propTypes = {
  templates: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
