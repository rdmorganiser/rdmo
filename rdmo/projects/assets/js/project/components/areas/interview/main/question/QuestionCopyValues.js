import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { copyValue } from '../../../../../actions/interviewActions'
import { isEmptyValue } from '../../../../../utils/value'

const QuestionCopyValues = ({ question, sets, values, siblings, currentSet }) => {
  const dispatch = useDispatch()

  const button = question.widget_type == 'checkbox' ? (
    <LinkButton
      className="question-copy-values-button"
      title={gettext('Apply this answer to all tabs where this question is empty')}
      aria-label={gettext('Apply this answer to all tabs where this question is empty')}
      onClick={() => dispatch(copyValue(question, ...values))}
    >
      <i className="bi bi-arrow-right-circle" aria-hidden="true"></i>
    </LinkButton>
  ) : (
    <button
      type="button"
      className="btn btn-outline-primary btn-sm question-copy-values-button"
      onClick={() => dispatch(copyValue(question, ...values))}
    >
      <div className="d-flex align-items-center gap-2">
        <i className="bi bi-arrow-right-circle" aria-hidden="true"></i>
        <span>{gettext('Apply to all')}</span>
      </div>
    </button>
  )

  const hasValues = values.some((value) => !isEmptyValue(value))

  const hasEmptySiblingSet = sets.filter((set) => (
    (set.set_prefix == currentSet.set_prefix) &&
      (set.set_index != currentSet.set_index) &&
      (set.element.elements.includes(question))
  )).some((set) => {
    // loop over all other sets and filter siblings accordingly
    const setSiblings = siblings.filter((value) => (
      (value.set_prefix == set.set_prefix) &&
        (value.set_index == set.set_index)
    ))

    // check if this set has no siblings at all (for checkboxes) or if every sibling is empty
    return setSiblings.every((value) => isEmptyValue(value))
  })

  return (
    question.is_collection &&
    question.set_collection &&
    hasValues &&
    hasEmptySiblingSet &&
    button
  )
}

QuestionCopyValues.propTypes = {
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  currentSet: PropTypes.object.isRequired,
}

export default QuestionCopyValues
