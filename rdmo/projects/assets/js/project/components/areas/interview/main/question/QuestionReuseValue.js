import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { LinkButton, Modal } from 'rdmo/core/assets/js/components'
import useLsState from 'rdmo/core/assets/js/hooks/useLsState'

import { updateValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'

import Search from '../Search'

const QuestionReuseValue = ({ question, value }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()

  const initialFormValues = {
    value: '',
    snapshot: false
  }

  const [show, setShow] = useState(false)
  const [
    formValues, setFormValues, initFormValues
  ] = useLsState('rdmo.interview.reuse', initialFormValues, ['value'])
  const [formErrors, setFormErrors] = useState([])

  const handleSubmit = (mode) => {
    if (isEmpty(formValues.value)) {
      setFormErrors([gettext('No answer to reuse selected.')])
    } else {
      const { text, option, external_id } = formValues.value

      if (mode == 'append') {
        dispatch(updateValue(value, { text: `${value.text} ${text}`, option, external_id }))
      } else if (mode == 'replace') {
        dispatch(updateValue(value, { text, option, external_id }))
      }

      setShow(false)
    }
  }

  useEffect(() => {
    if (show) {
      initFormValues()
    }
  }, [show])

  useEffect(() => {
    if (!isEmpty(formValues.value)) {
      // remove the hasError flag if an inputValue is entered
      setFormErrors([])
    }
  }, [formValues, formValues.value])

  const title = gettext('Reuse answer')

  const extraButtons = (
    <>
      {
        ['text', 'textarea'].includes(question.widget_type) && (
          <button type="button" className="btn btn-primary" onClick={() => handleSubmit('append')}>
            {gettext('Append')}
          </button>
        )
      }
      <button type="button" className="btn btn-primary" onClick={() => handleSubmit('replace')}>
        {gettext('Replace')}
      </button>
    </>
  )

  return !readOnly && (
    <>
      <LinkButton
        className="question-reuse-value-button"
        title={title}
        aria-label={title}
        onClick={() => setShow(true)}
      >
        <i className="bi bi-arrow-down-circle" aria-hidden="true"></i>
      </LinkButton>

      <Modal
        title={gettext('Reuse answer')}
        show={show}
        extraButtons={extraButtons}
        onClose={() => setShow(false)}
      >
        <div className={classNames({'form-group': true, 'has-error': formErrors.value })}>
          <label htmlFor="project-interview-page-tabs-modal-form-import">
            {gettext('Answer')}
          </label>

          <Search
            question={question}
            attribute={value.attribute}
            values={formValues}
            errors={formErrors}
            setValues={setFormValues}
          />

          <p className="help-block mb-0">
            {
              gettext('You can reuse an answer from a similar question in any ' +
                   'project you have access to.')
            }
          </p>
        </div>
      </Modal>
    </>
  )
}

QuestionReuseValue.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
}

export default QuestionReuseValue
