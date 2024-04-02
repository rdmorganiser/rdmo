import React from 'react'
import PropTypes from 'prop-types'

const QuestionSet = ({ questionset }) => {
  console.log(questionset)

  return (
    <div className="interview-questionset">

    </div>
  )
}

QuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSet
