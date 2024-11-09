import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const QuestionReuseValue = ({ value, updateValue }) => {

  const initial = {
    copySetValue: '',
    snapshot: false
  }

  const [show, setShow] = useState(false)
  const [formValues, setFormValues] = useState(initial)
  const [formErrors, setFormErrors] = useState([])

  const handleSubmit = () => {
    if (isEmpty(formValues.copySetValue)) {
      setFormErrors({ copySetValue: true })
    } else {
      const { text, option, external_id } = formValues.copySetValue
      updateValue(value, { text, option, external_id })
      setShow(false)
    }
  }

  // init the form values
  useEffect(() => {
    if (show) {
      setFormValues(initial)
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(formValues.copySetValue)) {
      setFormErrors({ copySetValue: false })
    }
  }, [formValues, formValues.copySetValue])

  return <>
    <button type="button" className="btn btn-link btn-reuse-value" onClick={() => setShow(true)}>
      <i className="fa fa-arrow-circle-down fa-btn"></i>
    </button>

    <Modal title={gettext('Reuse answer')} show={show} submitLabel={gettext('Reuse answer')}
           submitProps={{className: 'btn btn-primary'}}
           onClose={() => setShow(false)} onSubmit={handleSubmit}>
      <div className={classNames({'form-group': true, 'has-error': formErrors.copySetValue })}>
        <label className="control-label" htmlFor="interview-page-tabs-modal-form-import">
          {gettext('Reuse answer')}
        </label>

        <Search attribute={value.attribute} values={formValues} setValues={setFormValues} />

        <p className="help-block mb-0">
          {gettext('You can reuse an answer from a similar question in any ' +
                   'project you have access to.')}
        </p>
      </div>
    </Modal>
  </>
}

QuestionReuseValue.propTypes = {
  value: PropTypes.object.isRequired,
  updateValue: PropTypes.func.isRequired
}

export default QuestionReuseValue
