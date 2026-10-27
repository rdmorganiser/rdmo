import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

import { useReadOnly } from '../../../../../hooks'

const QuestionAddValueHelp = ({ question }) => {
  const readOnly = useReadOnly()

  return !readOnly && question.is_collection && question.widget_type != 'checkbox' && (
    <Template template="project_interview_add_value_help" />
  )
}

QuestionAddValueHelp.propTypes = {
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
