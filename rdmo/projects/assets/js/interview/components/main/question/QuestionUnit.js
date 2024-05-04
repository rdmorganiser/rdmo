import React from 'react'
import PropTypes from 'prop-types'
import { isUndefined } from 'lodash'

const QuestionUnit = ({ question, inputValue }) => {
  return (question.unit || !isUndefined(inputValue)) && (
    <div className="unit">
      {
        !isUndefined(inputValue) && (
          <>
            <span>{inputValue}</span>
            {' '}
          </>
        )
      }
      {
        question.unit && !isUndefined(inputValue) && (' ')
      }
      {
        question.unit && (
          <span title={gettext('The unit for this answer.')}>{question.unit}</span>
        )
      }
    </div>
  )
}

QuestionUnit.propTypes = {
  question: PropTypes.object.isRequired,
  inputValue: PropTypes.string,
}

export default QuestionUnit
