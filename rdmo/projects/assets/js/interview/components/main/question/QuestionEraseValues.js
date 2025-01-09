import React from 'react'
import PropTypes from 'prop-types'

const QuestionEraseValues = ({ values, disabled, deleteValue }) => {
  const handleEraseValue = () => {
    values.forEach((value) => deleteValue(value))
  }

  return !disabled && (
    <button type="button" className="btn btn-link btn-erase-value" onClick={handleEraseValue}
            title={gettext('Erase input')}>
      <i className="fa fa-eraser fa-btn"></i>
    </button>
  )
}

QuestionEraseValues.propTypes = {
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default QuestionEraseValues
