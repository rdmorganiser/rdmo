import React, { useState, useRef, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil, isUndefined } from 'lodash'

import ValueApi from '../../../api/ValueApi'

import Modal from 'rdmo/core/assets/js/components/Modal'
import Select from 'rdmo/core/assets/js/components/Select'

import useFocusEffect from '../../../hooks/useFocusEffect'


const PageHeadFormModal = ({ title, submitLabel, submitColor, show, attribute, initial, onClose, onSubmit }) => {

  const ref = useRef(null)

  const [values, setValues] = useState(initial)
  const [errors, setErrors] = useState([])
  const [options, setOptions] = useState([])

  const handleSubmit = () => {
    if (isEmpty(values.text) && !isNil(attribute)) {
      setErrors({ text: true })
    } else {
      onSubmit(values.text, values.copySetValue)
    }
  }

  useEffect(() => {
    if (show && !isNil(attribute)) {
      // update the form values
      setValues(initial)

      // fetch the values for this attribute from all projects and snapshots
      if (!isNil(initial)) {
        ValueApi.fetchValues({ attribute }).then(response => setOptions(response.map(value => ({
          value: value,
          label: value.text
        }))))
      }
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(values.text)) {
      setErrors({ text: false })
    }
  }, [values, values.text])

  // focus when the modal is shown
  useFocusEffect(ref, show)

  return (
    <Modal title={title} show={show} submitLabel={submitLabel} submitProps={{className: `btn btn-${submitColor}`}}
           onClose={onClose} onSubmit={handleSubmit} disableSubmit={errors}>
      {
        isNil(attribute) ? (
          <div>
            {gettext('You can add a new tab using the create button.')}
          </div>
        ) : (
          <>
            <div className={classNames({'form-group': true, 'has-error': errors.text })}>
              <label className="control-label" htmlFor="interview-page-tabs-modal-form-title">
                {gettext('Name')}
              </label>
              <input
                ref={ref}
                className="form-control"
                id="interview-page-tabs-modal-form-title"
                type="text"
                value={values.text}
                onChange={(event) => setValues({ ...values, text: event.target.value })}
                onKeyPress={(event) => {
                  if (event.code === 'Enter') {
                    handleSubmit()
                  }
                }}
              />

              <p className="help-block">{gettext('Please give the tab a meaningful name.')}</p>
            </div>

            {
              !isUndefined(values.copySetValue) && (
                <div className={classNames({'form-group': true, 'has-error': errors.copySetValue })}>
                  <label className="control-label" htmlFor="interview-page-tabs-modal-form-import">
                    {gettext('Import answers')}
                  </label>
                  <Select
                    options={options}
                    onChange={(id) => setValues({ ...values, copySetValue: id })}
                    value={values.copySetValue}
                  />

                  <p className="help-block">{gettext('You can fill the tab with answers from a similar tab in this or another project.')}</p>
                </div>
              )
            }
          </>
        )
      }
    </Modal>
  )
}

PageHeadFormModal.propTypes = {
  title: PropTypes.string.isRequired,
  submitLabel: PropTypes.string.isRequired,
  submitColor: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  attribute: PropTypes.number,
  initial: PropTypes.object,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
}

export default PageHeadFormModal
