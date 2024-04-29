import React from 'react'
import PropTypes from 'prop-types'

const QuestionRemoveValue = ({ value, deleteValue }) => {
  return (
    <button type="button" className="btn btn-link btn-remove-value" onClick={() => deleteValue(value)}>
      <i className="fa fa-times fa-btn"></i>
    </button>
  )
}

QuestionRemoveValue.propTypes = {
  value: PropTypes.object.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default QuestionRemoveValue
