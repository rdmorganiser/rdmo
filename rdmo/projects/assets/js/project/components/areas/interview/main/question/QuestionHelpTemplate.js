import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionHelpTemplate = ({ show }) => {
  return show && <Template template="project_interview_question_help" />
}

QuestionHelpTemplate.propTypes = {
  show: PropTypes.bool.isRequired,
}

export default QuestionHelpTemplate
