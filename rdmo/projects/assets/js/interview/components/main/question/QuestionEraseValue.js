import React from 'react'
import PropTypes from 'prop-types'

const QuestionEraseValue = ({ value, updateValue }) => {
  const handleEraseValue = () => {
    updateValue(value, {})
  }

  return (
    <button type="button" className="btn btn-link btn-erase-value" onClick={handleEraseValue}
            title={gettext('Erase input')}>
      <i className="fa fa-eraser fa-btn"></i>
    </button>
  )
}

QuestionEraseValue.propTypes = {
  value: PropTypes.object.isRequired,
  updateValue: PropTypes.func.isRequired
}

export default QuestionEraseValue
