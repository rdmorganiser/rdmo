import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { copyValue } from '../../../../../actions/interviewActions'
import { isEmptyValue } from '../../../../../utils/value'

const QuestionCopyValue = ({ question, value, siblings }) => {
  const dispatch = useDispatch()
  const title = gettext('Apply this answer to all tabs where this question is empty')

  return (
    question.set_collection &&
    !question.is_collection &&
    !isEmptyValue(value) &&
    siblings.some((value) => isEmptyValue(value)) && (
      <LinkButton
        className="question-copy-value-button"
        title={title}
        aria-label={title}
        onClick={() => dispatch(copyValue(question, value))}
      >
        <i className="bi bi-arrow-right-circle" aria-hidden="true"></i>
      </LinkButton>
    )
  )
}

QuestionCopyValue.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  siblings: PropTypes.array.isRequired,
}

export default QuestionCopyValue
