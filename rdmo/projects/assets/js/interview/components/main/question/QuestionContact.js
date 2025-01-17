import React from 'react'
import PropTypes from 'prop-types'

const QuestionContact = ({ settings, question, values, fetchContact }) => {
  return settings.project_contact && (
    <button className="btn btn-link btn-contact" title={gettext('Contact support.')}
            onClick={() => fetchContact({ question, values })}>
      <i className="fa fa-commenting-o" aria-hidden="true"></i>
    </button>
  )
}

QuestionContact.propTypes = {
  settings: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  fetchContact: PropTypes.func.isRequired,
}

export default QuestionContact
