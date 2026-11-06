import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

import { useReadOnly } from '../../../../../hooks'

const QuestionSetAddSetHelp = ({ questionset }) => {
  const readOnly = useReadOnly()

  return !readOnly && questionset.is_collection && (
    <Template template="project_interview_add_set_help" />
  )
}

QuestionSetAddSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired,
}

export default QuestionSetAddSetHelp
