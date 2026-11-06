import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Modal from 'rdmo/core/assets/js/components/Modal'
import Template from 'rdmo/core/assets/js/components/Template'

import { closeContact, sendContact } from '../../../../actions/contactActions'

const Contact = () => {
  const dispatch = useDispatch()
  const contact = useSelector((state) => state.contact)

  const { showModal, values: initialValues, errors } = contact

  const [values, setValues] = useState({})

  useEffect(() => setValues(initialValues), [initialValues])

  const onSubmit = (event) => {
    event.preventDefault()
    dispatch(sendContact(values))
  }

  const onClose = () => dispatch(closeContact())

  return (
    <Modal
      show={showModal}
      title={gettext('Contact support')}
      submitLabel={gettext('Send message')}
      onSubmit={onSubmit}
      onClose={onClose}
      size="modal-lg"
    >
      <Template template="project_interview_contact_help" />
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label htmlFor="project-interview-question-contact-subject">Subject</label>
          <input
            type="text"
            id="project-interview-question-contact-subject"
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
          <label htmlFor="project-interview-question-contact-message">Message</label>
          <textarea
            rows="12"
            id="project-interview-question-contact-message"
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
  )
}

export default Contact
