import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const PageHeadReuseModal = ({ title, show, attribute, onClose, onSubmit }) => {

  const label = gettext('Reuse answers')

  const initialValues = {
    value: '',
    project: '',
    snapshot: false
  }

  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState([])

  const handleSubmit = () => {
    if (isEmpty(values.value)) {
      setErrors({ value: true })
    } else {
      onSubmit(values.value)
    }
  }

  useEffect(() => {
    if (show) {
      setValues(initialValues)
    }
  }, [show])

  useEffect(() => {
    if (!isEmpty(values.value)) {
      // remove the hasError flag if an inputValue is entered
      setErrors({ value: false })
    }
  }, [values, values.value])

  return (
    <Modal title={title} show={show} submitLabel={label} submitProps={{className: 'btn btn-primary'}}
           onClose={onClose} onSubmit={handleSubmit}>
      <div className={classNames({'form-group': true, 'has-error': errors.value })}>
        <label className="control-label">
          {label}
        </label>

        <Search attribute={attribute} values={values} setValues={setValues} />

        <p className="help-block mb-0">
          {gettext('You can populate this tab with answers from a similar tab in any ' +
                   'project you have access to. This only affects questions that ' +
                   'don\'t already have an answer.')}
        </p>
      </div>
    </Modal>
  )
}

PageHeadReuseModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  attribute: PropTypes.number,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
}

export default PageHeadReuseModal
