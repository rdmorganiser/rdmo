import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import Template from 'rdmo/core/assets/js/components/Template'

import { hasAddValueHelp } from '../../../../../utils/question'

const QuestionAddValueHelp = ({ question, show }) => {
  const templates = useSelector((state) => state.templates)
  const readOnly = useSelector(selectReadOnly)

  return show && hasAddValueHelp(question, templates, readOnly) && (
    <div className="font-small text-muted mb-2">
      <Template template="project_interview_add_value_help" />
    </div>
  )
}

QuestionAddValueHelp.propTypes = {
  question: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
}

export default QuestionAddValueHelp
