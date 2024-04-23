import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'
import isEmpty from 'lodash/isEmpty'

import Modal from 'rdmo/core/assets/js/components/Modal'

const PageHeadFormModal = ({ title, show, initial, onClose, onSubmit }) => {

  const [inputValue, setInputValue] = useState('')
  const [hasError, setHasError] = useState(false)
  const submitText = isNil(initial) ? gettext('Create') : gettext('Update')
  const submitColor = isNil(initial) ? 'success' : 'primary'

  const handleSubmit = () => {
    if (isEmpty(inputValue)) {
      setHasError(true)
    } else {
      onSubmit(inputValue)
    }
  }

  // update the inputValue when the modal ist shown
  useEffect(() => {
    if (show) {
      setInputValue(initial || '')
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(inputValue)) {
      setHasError(false)
    }
  }, [inputValue])

  return (
    <Modal title={title} show={show} submitText={submitText} submitColor={submitColor}
           onClose={onClose} onSubmit={handleSubmit} disableSubmit={hasError}>
      {
        isNil(initial) ? (
          <div>
            {gettext('You can add a new tab using the create button.')}
          </div>
        ) : (
          <div className={classNames({'form-group': true, 'has-error': hasError })}>
            <label className="control-label" htmlFor="interview-page-tabs-modal-form-title">
              {gettext('Name')}
            </label>
            <input
              className="form-control"
              id="interview-page-tabs-modal-form-title"
              type="text"
              value={inputValue}
              onChange={(event) => setInputValue(event.target.value)}
            />

            <p className="help-block">{gettext('Please give the tab a meaningful name.')}</p>
          </div>
        )
      }
    </Modal>
  )
}

PageHeadFormModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  initial: PropTypes.string,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
}

export default PageHeadFormModal
