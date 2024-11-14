import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import useLsState from 'rdmo/core/assets/js/hooks/useLsState'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const QuestionReuseValue = ({ page, question, value, updateValue }) => {
  const initialFormValues = {
    value: ''
  }

  const [show, setShow] = useState(false)
  const [
    formValues, setFormValues, initFormValues
  ] = useLsState('rdmo.interview.reuse', initialFormValues, ['value'])
  const [formErrors, setFormErrors] = useState([])

  const handleSubmit = (mode) => {
    if (isEmpty(formValues.value)) {
      setFormErrors({ value: true })
    } else {
      const { text, option, external_id } = formValues.value

      if (mode == 'append') {
        updateValue(value, { text: `${value.text} ${text}`, option, external_id })
      } else if (mode == 'replace') {
        updateValue(value, { text, option, external_id })
      }

      setShow(false)
    }
  }

  // init the form values
  useEffect(() => {
    if (show) {
      initFormValues()
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(formValues.value)) {
      setFormErrors({ value: false })
    }
  }, [formValues, formValues.value])

  const modalButtons = <>
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

  return <>
    <button type="button" className="btn btn-link btn-reuse-value" onClick={() => setShow(true)}>
      <i className="fa fa-arrow-circle-down fa-btn"></i>
    </button>

    <Modal title={gettext('Reuse answer')} show={show} buttons={modalButtons}
           onClose={() => setShow(false)} >
      <div className={classNames({'form-group': true, 'has-error': formErrors.value })}>
        <label className="control-label" htmlFor="interview-page-tabs-modal-form-import">
          {gettext('Answer')}
        </label>

        <Search
          page={page}
          attribute={value.attribute}
          values={formValues}
          setValues={setFormValues}
        />

        <p className="help-block mb-0">
          {gettext('You can reuse an answer from a similar question in any ' +
                   'project you have access to.')}
        </p>
      </div>
    </Modal>
  </>
}

QuestionReuseValue.propTypes = {
  page: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  updateValue: PropTypes.func.isRequired
}

export default QuestionReuseValue
