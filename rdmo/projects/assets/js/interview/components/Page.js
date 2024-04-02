import React from 'react'
import PropTypes from 'prop-types'

import Question from '../components/Question'
import QuestionSet from '../components/Question'

const Page = ({ page }) => {
  return (
    <div className="interview-page">
        <h2>
            {page.title}
        </h2>
        {
          page.elements.map((element, elementIndex) => {
            if (element.model == 'questions.questionset') {
              return <QuestionSet key={elementIndex} questionset={element}
              />
            } else {
              return <Question key={elementIndex} question={element}
              />
            }
          })
        }
    </div>
  )
}

Page.propTypes = {
  page: PropTypes.object.isRequired
}

export default Page
