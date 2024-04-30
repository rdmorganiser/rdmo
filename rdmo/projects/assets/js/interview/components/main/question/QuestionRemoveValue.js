import React from 'react'
import PropTypes from 'prop-types'

const QuestionRemoveValue = ({ question, values, value, disabled, deleteValue }) => {
  return !disabled && (question.is_collection || values.length > 1) && (
    <button type="button" className="btn btn-link btn-remove-value" onClick={() => deleteValue(value)}>
      <i className="fa fa-times fa-btn"></i>
    </button>
  )
}

QuestionRemoveValue.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default QuestionRemoveValue
