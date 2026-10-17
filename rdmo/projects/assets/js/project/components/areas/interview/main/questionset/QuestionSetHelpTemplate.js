import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

const QuestionSetHelpTemplate = () => {
  const templates = useSelector((state) => state.templates)

  return <Html html={templates.project_interview_questionset_help} />
}

export default QuestionSetHelpTemplate
