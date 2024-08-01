import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionHelpTemplate = ({ templates }) => {
  return <Html html={templates.project_interview_question_help} />
}

QuestionHelpTemplate.propTypes = {
  templates: PropTypes.object.isRequired
}

export default QuestionHelpTemplate
