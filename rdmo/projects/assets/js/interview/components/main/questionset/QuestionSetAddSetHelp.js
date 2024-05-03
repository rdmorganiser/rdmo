import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionSetAddSetHelp = ({ templates, questionset }) => {
  return questionset.is_collection && (
    <Template template={templates.project_interview_add_set_help} />
  )
}

QuestionSetAddSetHelp.propTypes = {
  templates: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired
}

export default QuestionSetAddSetHelp
