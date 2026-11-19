import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import { deleteValue } from '../../../../../actions/interviewActions'

const QuestionEraseValues = ({ values }) => {
  const dispatch = useDispatch()
  const readOnly = useSelector(selectReadOnly)
  const title = gettext('Erase input')

  const handleEraseValue = () => {
    values.forEach((value) => dispatch(deleteValue(value)))
  }

  return !readOnly && (
    <LinkButton
      className="question-erase-values-button"
      title={title}
      aria-label={title}
      onClick={handleEraseValue}
    >
      <i className="bi bi-eraser" aria-hidden="true"></i>
    </LinkButton>
  )
}

QuestionEraseValues.propTypes = {
  values: PropTypes.array.isRequired,
}

export default QuestionEraseValues
