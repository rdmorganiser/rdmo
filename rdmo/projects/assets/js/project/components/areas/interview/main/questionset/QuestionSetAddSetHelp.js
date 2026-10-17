import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { useReadOnly } from '../../../../../hooks'

const QuestionSetAddSetHelp = ({ questionset }) => {
  const templates = useSelector((state) => state.templates)
  const readOnly = useReadOnly()

  return !readOnly && questionset.is_collection && (
    <Html html={templates.project_interview_add_set_help} />
  )
}

QuestionSetAddSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired,
}

export default QuestionSetAddSetHelp
