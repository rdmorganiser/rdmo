import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { useReadOnly } from '../../../../../hooks'

const QuestionAddValueHelp = ({ question }) => {
  const templates = useSelector((state) => state.templates)
  const readOnly = useReadOnly()

  return !readOnly && question.is_collection && question.widget_type != 'checkbox' && (
    <Html html={templates.project_interview_add_value_help} />
  )
}

QuestionAddValueHelp.propTypes = {
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
