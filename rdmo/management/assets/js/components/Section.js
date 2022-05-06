import React, { Component} from 'react'
import PropTypes from 'prop-types'

import QuestionSet from './QuestionSet'

const Section = ({ section }) => {
    return (
        <div>
            <h3>{section.title}</h3>
            <p>{section.help}</p>
            {
                section.questionsets.map((questionset, index) => (
                    <QuestionSet questionset={questionset} key={index} />
                ))
            }
        </div>
    )
}

Section.propTypes = {
  section: PropTypes.object.isRequired
}

export default Section
