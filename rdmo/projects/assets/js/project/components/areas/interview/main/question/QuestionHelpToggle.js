import React from 'react'
import PropTypes from 'prop-types'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { getQuestionHelpId } from '../../../../../utils/question'

const QuestionHelpToggle = ({ question, show, onClick }) => {
  return (
    <LinkButton
      className="text-muted"
      title={show ? gettext('Hide help') : gettext('Show help')}
      aria-expanded={show}
      aria-controls={getQuestionHelpId(question)}
      onClick={onClick}
    >
      {gettext('Help')} <i className="bi bi-info-circle"></i>
    </LinkButton>
  )
}

QuestionHelpToggle.propTypes = {
  question: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

export default QuestionHelpToggle
