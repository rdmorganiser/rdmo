import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { initRange } from '../../../../../utils/value'

const QuestionEraseValue = ({ question, value }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()
  const title = gettext('Erase input')

  const handleEraseValue = () => {
    if (question.widget_type == 'range') {
      initRange(question, {})
    }

    dispatch(updateValue(value, {}))
  }

  return !readOnly && (
    <LinkButton
      className="question-erase-value-button"
      title={title}
      aria-label={title}
      onClick={handleEraseValue}
    >
      <i className="bi bi-eraser" aria-hidden="true"></i>
    </LinkButton>
  )
}

QuestionEraseValue.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
}

export default QuestionEraseValue
