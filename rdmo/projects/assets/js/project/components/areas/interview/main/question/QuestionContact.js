import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'

import { fetchContact } from '../../../../../actions/contactActions'

const QuestionContact = ({ question, values }) => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)

  return settings.project_contact && (
    <LinkButton
      type="button"
      title={gettext('Contact support')}
      aria-label={gettext('Contact support')}
      onClick={() => dispatch(fetchContact({ question, values }))}
    >
      <i className="bi bi-chat-dots" aria-hidden="true"></i>
    </LinkButton>
  )
}

QuestionContact.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
}

export default QuestionContact
