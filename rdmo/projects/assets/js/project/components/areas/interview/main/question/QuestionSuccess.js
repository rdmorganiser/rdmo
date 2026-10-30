import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const QuestionSuccess = ({ value }) => {
  return (
    <div className={
      classNames('question-success text-success', {
        'show': value.success
      })
    }>
      <i className="bi bi-check-circle" aria-hidden="true"></i>
    </div>
  )
}

QuestionSuccess.propTypes = {
  value: PropTypes.object.isRequired,
}

export default QuestionSuccess
