import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Question = ({ question }) => {
    return (
        <div>
            <strong>{question.text}</strong>
            <p>{question.help}</p>
        </div>
    )
}

Question.propTypes = {
  question: PropTypes.object.isRequired
}

export default Question
