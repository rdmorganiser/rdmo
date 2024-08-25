import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionSetHelpTemplate = ({ templates }) => {
  return <Html html={templates.project_interview_questionset_help} />
}

QuestionSetHelpTemplate.propTypes = {
  templates: PropTypes.object
}

export default QuestionSetHelpTemplate
