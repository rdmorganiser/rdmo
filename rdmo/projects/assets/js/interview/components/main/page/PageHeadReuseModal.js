import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import useLsState from 'rdmo/core/assets/js/hooks/useLsState'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const PageHeadReuseModal = ({ show, attribute, onClose, onSubmit }) => {

  const initialValues = {
    value: ''
  }

  const [values, setValues, initValues] = useLsState('rdmo.interview.reuse', initialValues, ['value'])
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
      initValues()
    }
  }, [show])

  useEffect(() => {
    if (!isEmpty(values.value)) {
      // remove the hasError flag if an inputValue is entered
      setErrors({ value: false })
    }
  }, [values, values.value])

  return (
    <Modal title={gettext('Reuse answers')} show={show} submitLabel={gettext('Reuse')}
           submitProps={{className: 'btn btn-primary'}}
           onClose={onClose} onSubmit={handleSubmit}>
      <div className={classNames({'form-group': true, 'has-error': errors.value })}>
        <label className="control-label">
          {gettext('Answers')}
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
