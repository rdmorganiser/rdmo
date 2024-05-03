import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionAddValueHelp = ({ templates, question }) => {
  return question.is_collection && (
    <Template template={templates.project_interview_add_value_help} />
  )
}

QuestionAddValueHelp.propTypes = {
  templates: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
