import React, { Component} from 'react'
import PropTypes from 'prop-types'

import Question from './Question'

const QuestionSet = ({ questionset }) => {
    return (
        <div>
            <h4>{questionset.title}</h4>
            <p>{questionset.help}</p>
            {
                questionset.questions.map((question, index) => (
                    <Question question={question} key={index} />
                ))
            }
        </div>
    )
}

QuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSet
