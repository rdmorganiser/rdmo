import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import Template from 'rdmo/core/assets/js/components/Template'

const QuestionSetAddSetHelp = ({ questionset }) => {
  const readOnly = useSelector(selectReadOnly)

  return !readOnly && questionset.is_collection && (
    <Template template="project_interview_add_set_help" />
  )
}

QuestionSetAddSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired,
}

export default QuestionSetAddSetHelp
