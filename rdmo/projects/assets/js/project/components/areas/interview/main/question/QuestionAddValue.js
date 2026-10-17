import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import { maxBy, upperFirst } from 'lodash'

import { createValue } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { initRange } from '../../../../../utils/value'

const AddValue = ({ question, values, currentSet }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()
  const title = gettext('Add answer')

  const handleClick = () => {
    const lastValue = maxBy(values, (v) => v.collection_index)
    const collectionIndex = lastValue ? lastValue.collection_index + 1 : 0

    const value = {
      attribute: question.attribute,
      set_prefix: currentSet.set_prefix,
      set_index: currentSet.set_index,
      set_collection: question.set_collection,
      collection_index: collectionIndex,
      unit: question.unit,
      value_type: question.value_type
    }

    if (question.widget_type == 'range') {
      initRange(question, value)
    }

    dispatch(createValue(value))
  }

  return !readOnly && question.is_collection && (
    <button
      type="button"
      className="btn btn-outline-success btn-sm question-add-value-button"
      onClick={handleClick}
      title={title}
      aria-label={title}
    >
      <div className="d-flex align-items-center gap-2">
        <i className="bi bi-plus-circle" aria-hidden="true"></i>
        <span>{upperFirst(question.verbose_name)}</span>
      </div>
    </button>
  )
}

AddValue.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired,
}

export default AddValue
