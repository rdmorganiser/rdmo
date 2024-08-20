import React from 'react'
import PropTypes from 'prop-types'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValues = ({ question, values, siblings, copyValue }) => {
  const handleCopyValues = () => {
    values.forEach((value) => copyValue(value))
  }

  const button = question.widget_type == 'checkbox' ? (
    <button className="btn btn-link btn-apply-to-all" onClick={handleCopyValues}
            title={gettext('Apply this answer to all tabs where this question is empty')}>
      <i className="fa fa-arrow-circle-right fa-btn"></i>
    </button>
  ) : (
    <button type="button" className="btn btn-primary btn-xs copy-value-button ml-10" onClick={handleCopyValues}>
      <i className="fa fa-arrow-circle-right fa-btn"></i> {gettext('Apply to all')}
    </button>
  )

  return (
    question.is_collection &&
    question.set_collection &&
    values.some((v) => !isEmptyValue(v)) &&
    siblings.some((value) => isEmptyValue(value)) &&
    button
  )
}

QuestionCopyValues.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  copyValue: PropTypes.func.isRequired
}

export default QuestionCopyValues
