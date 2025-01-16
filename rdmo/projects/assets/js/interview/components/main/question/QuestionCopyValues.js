import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValues = ({ question, sets, values, siblings, currentSet, copyValue }) => {
  const button = question.widget_type == 'checkbox' ? (
    <button className="btn btn-link btn-apply-to-all" onClick={() => copyValue(...values)}
            title={gettext('Apply this answer to all tabs where this question is empty')}>
      <i className="fa fa-arrow-circle-right fa-btn"></i>
    </button>
  ) : (
    <button type="button" className="btn btn-primary btn-xs copy-value-button ml-10" onClick={() => copyValue(...values)}>
      <i className="fa fa-arrow-circle-right fa-btn"></i> {gettext('Apply to all')}
    </button>
  )

  const hasValues = values.some((value) => !isEmptyValue(value))

  const hasEmptySiblings = sets.filter((set) => (
      (set.set_prefix == currentSet.set_prefix) &&
      (set.set_index != currentSet.set_index)
    )).some((set) => {
      // loop over all other sets and filter siblings accordingly
      const setSiblings = siblings.filter((value) => (
        (value.set_prefix == set.set_prefix) &&
        (value.set_index == set.set_index)
      ))

      // check if this set has no sibling at all (for checkboxes) or if they are empty
      return isEmpty(setSiblings) || setSiblings.some((value) => isEmptyValue(value))
    })

  return (
    question.is_collection &&
    question.set_collection &&
    hasValues &&
    hasEmptySiblings &&
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
