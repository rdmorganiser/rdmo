import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionSetAddSetHelp = ({ templates, questionset, disabled }) => {
  return !disabled && questionset.is_collection && (
    <Html html={templates.project_interview_add_set_help} />
  )
}

QuestionSetAddSetHelp.propTypes = {
  templates: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  disabled: PropTypes.bool.isRequired
}

export default QuestionSetAddSetHelp
