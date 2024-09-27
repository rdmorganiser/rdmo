import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Html from 'rdmo/core/assets/js/components/Html'

const Contact = ({ templates, contact, sendContact, closeContact }) => {
  const { showModal, values: initialValues, errors } = contact

  const [values, setValues] = useState({})

  useEffect(() => setValues(initialValues), [initialValues])

  const onSubmit = (event) => {
    event.preventDefault()
    sendContact(values)
  }

  const onClose = () => closeContact()

  return (
    <>
      <Modal
        show={showModal}
        title={gettext('Contact support')}
        submitLabel={gettext('Send message')}
        onSubmit={onSubmit}
        onClose={onClose}
        modalProps={{
          bsSize: 'lg'
        }}>
          <Html html={templates.project_interview_contact_help} />
          <form onSubmit={onSubmit}>
            <div className="form-group">
              <label htmlFor="interview-question-contact-subject">Subject</label>
              <input
                type="text"
                id="interview-question-contact-subject"
                className="form-control"
                value={values.subject || ''}
                onChange={event => setValues({ ...values, subject: event.target.value })}
              />
              <ul className="help-block list-unstyled">
                {
                  errors && errors.subject && errors.subject.map((error, errorIndex) => (
                    <li key={errorIndex} className="text-danger">{errors.subject}</li>
                  ))
                }
              </ul>
            </div>
            <div className="form-group">
              <label htmlFor="interview-question-contact-message">Message</label>
              <textarea
                rows="12"
                id="interview-question-contact-message"
                className="form-control"
                value={values.message || ''}
                onChange={event => setValues({...values, message: event.target.value })}
              />
              <ul className="help-block list-unstyled">
                {
                  errors && errors.message && errors.message.map((error, errorIndex) => (
                    <li key={errorIndex} className="text-danger">{errors.message}</li>
                  ))
                }
              </ul>
            </div>
          </form>
      </Modal>
    </>
  )
}

Contact.propTypes = {
  templates: PropTypes.object.isRequired,
  contact: PropTypes.object.isRequired,
  sendContact: PropTypes.func.isRequired,
  closeContact: PropTypes.func.isRequired
}

export default Contact
