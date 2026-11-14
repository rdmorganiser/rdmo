import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import { getQuestionHelpId, hasAddValueHelp } from '../../../../../utils/question'

const QuestionHelpToggle = ({ question, currentSet, show, onClick }) => {
  const templates = useSelector((state) => state.templates)
  const readOnly = useSelector(selectReadOnly)

  return (
    !isEmpty(question.help) ||
    !isEmpty(templates.project_interview_question_help) ||
    hasAddValueHelp(question, templates, readOnly)
  ) && (
    <LinkButton
      className="text-muted"
      title={show ? gettext('Hide help') : gettext('Show help')}
      aria-expanded={show}
      aria-controls={getQuestionHelpId(question, currentSet)}
      onClick={onClick}
    >
      {gettext('Help')} <i className="bi bi-info-circle"></i>
    </LinkButton>
  )
}

QuestionHelpToggle.propTypes = {
  question: PropTypes.object.isRequired,
  currentSet: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired
}

export default QuestionHelpToggle
