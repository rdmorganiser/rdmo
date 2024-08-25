import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const QuestionSuccess = ({ value }) => {
  return (
    <div className={classNames('success-indicator text-success', {
      'show': value.success
    })}>
      <i className="fa fa-check fa-btn"></i>
    </div>
  )
}

QuestionSuccess.propTypes = {
  value: PropTypes.object.isRequired,
}

export default QuestionSuccess
