import React, { useEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'

import useLsState from 'rdmo/core/assets/js/hooks/useLsState'

import Input from 'rdmo/core/assets/js/components/forms/Input'
import Modal from 'rdmo/core/assets/js/components/Modal'

import Search from '../Search'

const PageHeadFormModal = ({ title, submitLabel, submitColor, show, attribute, reuse, initial, onClose, onSubmit }) => {
  const inputRef = useRef(null)

  const initialValues = {
    text: initial || '',
    value: ''
  }

  const [values, setValues, initValues] = useLsState('rdmo.interview.reuse', initialValues, ['text', 'value'])
  const [errors, setErrors] = useState([])

  const handleSubmit = () => {
    if (isNil(attribute)) {
      onSubmit()
    } else {
      if (isEmpty(values.text)) {
        setErrors(['This field may not be blank.'])
      } else {
        onSubmit(values.text, values.value)
      }
    }
  }

  // init the form values
  useEffect(() => {
    if (show && !isNil(attribute)) {
      initValues()
    }
  }, [show])

  // remove the hasError flag if an inputValue is entered
  useEffect(() => {
    if (!isEmpty(values.text)) {
      setErrors([])
    }
  }, [values.text])

  return (
    <Modal
      title={title}
      show={show}
      submitLabel={submitLabel}
      submitProps={{className: `btn btn-${submitColor}`}}
      onClose={onClose}
      onSubmit={handleSubmit}
      onShown={() => inputRef.current?.focus()}
      disableSubmit={errors}
    >
      {
        isNil(attribute) ? (
          <div>
            {gettext('You can add a new tab using the create button.')}
          </div>
        ) : (
          <>
            <Input
              label={gettext('Name')}
              help={gettext('Please give the tab a meaningful name.')}
              value={values.text}
              inputRef={inputRef}
              onChange={(value) => setValues({ ...values, text: value })}
              onEnter={handleSubmit}
              errors={errors}
            />
            {
              reuse && (
                <div className={classNames({'form-group': true, 'has-error': errors.value })}>
                  <label>
                    {gettext('Reuse answers')}
                  </label>

                  <Search attribute={attribute} values={values} setValues={setValues} />

                  <p className="help-block mb-0">
                    {
                      gettext(
                        'You can populate this tab with answers from a similar tab in any ' +
                        'project you are allowed to access.'
                      )
                    }
                  </p>
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
  reuse: PropTypes.bool,
  initial: PropTypes.string,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
}

export default PageHeadFormModal
