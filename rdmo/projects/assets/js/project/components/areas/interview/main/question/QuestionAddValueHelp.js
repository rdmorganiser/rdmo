import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Template from 'rdmo/core/assets/js/components/Template'

import { isReadOnly } from '../../../../../../common/utils/permissions'

const QuestionAddValueHelp = ({ question }) => {
  const readOnly = useSelector((state) => isReadOnly(state.combinedPermissions))

  return !readOnly && question.is_collection && question.widget_type != 'checkbox' && (
    <Template template="project_interview_add_value_help" />
  )
}

QuestionAddValueHelp.propTypes = {
  question: PropTypes.object.isRequired,
}

export default QuestionAddValueHelp
