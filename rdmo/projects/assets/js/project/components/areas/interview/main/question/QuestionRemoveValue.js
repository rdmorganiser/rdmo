import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { isReadOnly } from '../../../../../../common/utils/permissions'
import { deleteValue } from '../../../../../actions/interviewActions'

const QuestionRemoveValue = ({ question, values, value }) => {
  const dispatch = useDispatch()
  const readOnly = useSelector((state) => isReadOnly(state.combinedPermissions))

  return !readOnly && (question.is_collection || values.length > 1) && (
    <LinkButton
      className="question-remove-value-button"
      title={gettext('Remove answer')}
      aria-label={gettext('Remove answer')}
      onClick={() => dispatch(deleteValue(value))}
    >
      <i className="bi bi-x-circle" aria-hidden="true"></i>
    </LinkButton>
  )
}

QuestionRemoveValue.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  value: PropTypes.object.isRequired,
}

export default QuestionRemoveValue
