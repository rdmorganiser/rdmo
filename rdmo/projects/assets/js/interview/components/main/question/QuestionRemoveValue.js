import React from 'react'
import PropTypes from 'prop-types'

const QuestionRemoveValue = ({ question, values, value, disabled, deleteValue }) => {
  return !disabled && (question.is_collection || values.length > 1) && (
    <button type="button" className="btn btn-link btn-remove-value" onClick={() => deleteValue(value)}
            title={gettext('Remove answer')} aria-label={gettext('Remove answer')}>
      <i className="fa fa-times fa-btn" aria-hidden="true"></i>
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
