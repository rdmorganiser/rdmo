import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionAddValueHelp = ({ question }) => {
  const readOnly = useSelector(selectReadOnly)

  return !readOnly && question.is_collection && question.widget_type != 'checkbox' && (
    <Template template="project_interview_add_value_help" />
  )
}

QuestionAddValueHelp.propTypes = {
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
