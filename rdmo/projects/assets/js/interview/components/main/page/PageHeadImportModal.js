import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const PageHeadImportModal = ({ title, show, attribute, onClose, onSubmit }) => {

  const initial = {
    copySetValue: '',
    snapshot: false
  }

  const [values, setValues] = useState(initial)
  const [errors, setErrors] = useState([])

  const handleSubmit = () => {
    if (isEmpty(values.copySetValue)) {
      setErrors({ copySetValue: true })
    } else {
      onSubmit(values.copySetValue)
    }
  }

  // init the form values
  useEffect(() => {
    if (show) {
      setValues(initial)
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(values.copySetValue)) {
      setErrors({ copySetValue: false })
    }
  }, [values, values.copySetValue])

  return (
    <Modal title={title} show={show} submitLabel="Copy values" submitProps={{className: 'btn btn-primary'}}
           onClose={onClose} onSubmit={handleSubmit}>
      <div className={classNames({'form-group': true, 'has-error': errors.copySetValue })}>
        <label className="control-label" htmlFor="interview-page-tabs-modal-form-import">
          {gettext('Copy answers')}
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

PageHeadImportModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  attribute: PropTypes.number,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
}

export default PageHeadImportModal
