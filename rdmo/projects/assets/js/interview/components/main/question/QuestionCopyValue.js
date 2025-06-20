import React from 'react'
import PropTypes from 'prop-types'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValue = ({ question, value, siblings, copyValue }) => {
  return (
    question.set_collection &&
    !question.is_collection &&
    !isEmptyValue(value) &&
    siblings.some((value) => isEmptyValue(value)) && (
      <button type="button" className="btn btn-link btn-apply-to-all" onClick={() => copyValue(question, value)}
              title={gettext('Apply this answer to all tabs where this question is empty')}
              aria-label={gettext('Apply this answer to all tabs where this question is empty')}>
        <i className="fa fa-arrow-circle-right fa-btn" aria-hidden="true"></i>
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
