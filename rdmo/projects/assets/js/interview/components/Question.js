import React from 'react'
import PropTypes from 'prop-types'

import Widget from './Widget'

const Question = ({ question }) => {
  return (
    <div className="interview-question">
      <Widget question={question} />
    </div>
  )
}

Question.propTypes = {
  question: PropTypes.object.isRequired
}

export default Question
