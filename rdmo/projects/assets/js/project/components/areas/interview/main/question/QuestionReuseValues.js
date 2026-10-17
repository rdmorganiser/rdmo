import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'

import { LinkButton, Modal } from 'rdmo/core/assets/js/components'
import useLsState from 'rdmo/core/assets/js/hooks/useLsState'

import { useReadOnly } from '../../../../../hooks'

import Search from '../Search'

const QuestionReuseValues = ({ question, values, onCreate, onUpdate, onDelete }) => {
  const readOnly = useReadOnly()
  const title = gettext('Reuse answers')

  const initialFormValues = {
    value: '',
    snapshot: false,
    collection: true
  }

  const [show, setShow] = useState(false)
  const [
    formValues, setFormValues, initFormValues
  ] = useLsState('rdmo.interview.reuse', initialFormValues, ['value', 'collection'])
  const [formErrors, setFormErrors] = useState([])

  const compareValues = (a, b) => (
    (a.set_prefix == b.set_prefix) &&
    (a.set_index == b.set_index) &&
    (
      (!isNil(a.option) && (a.option == b.option)) ||
      (!isEmpty(a.external_id) && (a.external_id == b.external_id))
    )
  )

  const handleSubmit = () => {
    if (isEmpty(formValues.value)) {
      setFormErrors([gettext('No answer to reuse selected.')])
    } else {
      values.forEach(value => {
        // look for the "same" value in the list of values from the search component
        const reusedValue = formValues.value.values.find(reusedValue => compareValues(value, reusedValue))
        if (isNil(reusedValue)) {
          // delete the value if it does not exist in the reused value
          onDelete(value)
        } else if (value.text != reusedValue.text) {
          // update the value if the additional text changed
          onUpdate(value, { text: reusedValue.text, option: value.option, external_id: value.external_id })
        }
      })

      const newValues = []
      formValues.value.values.forEach(reusedValue => {
        // look for the "same" value in the existing values
        const value = values.find(value => compareValues(value, reusedValue))
        if (isNil(value)) {
          newValues.push({ text: reusedValue.text, option: reusedValue.option, external_id: reusedValue.external_id })
        }
      })

      onCreate(newValues)
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
      setFormErrors([])
    }
  }, [formValues, formValues.value])

  return !readOnly && (
    <>
      <LinkButton
        className="question-reuse-values-button"
        title={title}
        aria-label={title}
        onClick={() => setShow(true)}
      >
        <i className="bi bi-arrow-down-circle" aria-hidden="true"></i>
      </LinkButton>

      <Modal
        title={gettext('Reuse answer')} show={show} submitLabel={gettext('Replace')}
        submitProps={{className: 'btn btn-primary'}}
        onClose={() => setShow(false)} onSubmit={handleSubmit}>
        <div className={classNames({'form-group': true, 'has-error': formErrors.value })}>
          <label htmlFor="project-interview-page-tabs-modal-form-import">
            {gettext('Answer')}
          </label>

          <Search
            question={question}
            attribute={question.attribute}
            values={formValues}
            errors={formErrors}
            setValues={setFormValues}
            collection={true}
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

QuestionReuseValues.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  onCreate: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
}

export default QuestionReuseValues
