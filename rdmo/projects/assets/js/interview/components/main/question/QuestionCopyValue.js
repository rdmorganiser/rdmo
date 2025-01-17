import React from 'react'
import PropTypes from 'prop-types'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValue = ({ question, value, siblings, copyValue }) => {
  return (
    question.set_collection &&
    !question.is_collection &&
    !isEmptyValue(value) &&
    siblings.some((value) => isEmptyValue(value)) && (
      <button className="btn btn-link btn-apply-to-all" onClick={() => copyValue(value)}
              title={gettext('Apply this answer to all tabs where this question is empty')}>
        <i className="fa fa-arrow-circle-right fa-btn"></i>
      </button>
    )
  )
}

QuestionCopyValue.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  siblings: PropTypes.array.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default QuestionCopyValue
