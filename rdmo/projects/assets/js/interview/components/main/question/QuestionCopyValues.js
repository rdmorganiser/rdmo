import React from 'react'
import PropTypes from 'prop-types'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValues = ({ question, sets, values, siblings, currentSet, copyValue }) => {
  const button = question.widget_type == 'checkbox' ? (
    <button className="btn btn-link btn-apply-to-all" onClick={() => copyValue(question, ...values)}
            title={gettext('Apply this answer to all tabs where this question is empty')}
            aria-label={gettext('Apply this answer to all tabs where this question is empty')}>
      <i className="fa fa-arrow-circle-right fa-btn" aria-hidden="true"></i>
    </button>
  ) : (
    <button type="button" className="btn btn-primary btn-xs copy-value-button ml-10" onClick={() => copyValue(question, ...values)}>
      <i className="fa fa-arrow-circle-right fa-btn" aria-hidden="true"></i> {gettext('Apply to all')}
    </button>
  )

  const hasValues = values.some((value) => !isEmptyValue(value, question.widget_type))

  const hasEmptySiblingSet = sets.filter((set) => (
      (set.set_prefix == currentSet.set_prefix) &&
      (set.set_index != currentSet.set_index) &&
      (set.element == question.parent)
    )).some((set) => {
      const setSiblings = siblings.filter((value) => (
        (value.set_prefix == set.set_prefix) &&
        (value.set_index == set.set_index)
      ))

      // check if this set has no siblings at all (e.g. checkboxes)
      // or if all existing siblings are empty for this widget
      return setSiblings.every(
        (value) => isEmptyValue(value, question.widget_type)
      )
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
  copyValue: PropTypes.func.isRequired
}

export default QuestionCopyValues
