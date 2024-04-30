import React from 'react'
import PropTypes from 'prop-types'
import { capitalize, maxBy } from 'lodash'

const AddValue = ({ question, values, currentSet, disabled, createValue }) => {
  const handleClick = () => {
    const lastValue = maxBy(values, (v) => v.collection_index)
    const collectionIndex = lastValue ? lastValue.collection_index + 1 : 0

    createValue({
      attribute: question.attribute,
      set_prefix: currentSet.set_prefix,
      set_index: currentSet.set_index,
      collection_index: collectionIndex
    })
  }

  return !disabled && question.is_collection && (
    <button type="button" className="btn btn-success add-value-button" onClick={handleClick}>
      <i className="fa fa-plus fa-btn"></i> {capitalize(question.verbose_name)}
    </button>
  )
}

AddValue.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired,
  disabled: PropTypes.bool.isRequired,
  createValue: PropTypes.func.isRequired
}

export default AddValue
