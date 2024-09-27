import React from 'react'
import PropTypes from 'prop-types'

const QuestionContact = ({ settings, question, values, fetchContact }) => {
  return settings.project_contact && (
    <div className="interview-question-contact">
      <button className="btn btn-link" title={gettext('Contact support.')}
              onClick={() => fetchContact({ question, values })}>
        <span className="badge badge-pill badge-primary">
          <i className="fa fa-question" aria-hidden="true"></i>
        </span>
      </button>
    </div>
  )
}

QuestionContact.propTypes = {
  settings: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  fetchContact: PropTypes.func.isRequired,
}

export default QuestionContact
