import React from 'react'
import PropTypes from 'prop-types'

import { isEmptyValue } from '../../../utils/value'

const QuestionCopyValues = ({ question, values, copyValue }) => {
  const handleCopyValues = () => {
    values.forEach((value) => copyValue(value))
  }

  console.log(values)

  return (
    question.set_collection && values.some((v) => !isEmptyValue(v)) && (
      <button className="btn btn-link btn-apply-to-all" onClick={handleCopyValues}
              title={gettext('Apply this answer to all tabs where this question is empty')}>
        <i className="fa fa-arrow-circle-right fa-btn"></i>
      </button>
    )
  )
}

QuestionCopyValues.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default QuestionCopyValues
