import React from 'react'
import PropTypes from 'prop-types'

// eslint-disable-next-line no-unused-vars
const QuestionSet = ({ questionset, values }) => {
  return (
    <div className="interview-questionset">

    </div>
  )
}

QuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired
}

export default QuestionSet
