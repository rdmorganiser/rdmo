import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import { maxBy, upperFirst } from 'lodash'

import { createSet } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'

const QuestionSetAddSet = ({ questionset, sets, setPrefix }) => {
  const dispatch = useDispatch()
  const readOnly = useReadOnly()

  const handleClick = () => {
    const lastSet = maxBy(sets, (s) => s.set_index)
    const setIndex = lastSet ? lastSet.set_index + 1 : 0

    dispatch(createSet({
      set_prefix: setPrefix,
      set_index: setIndex,
      element: questionset
    }))
  }

  return !readOnly && questionset.is_collection && (
    <button
      type="button" className="btn btn-outline-success btn-sm add-set-button"
      title={'Add block'} aria-label={'Add block'}
      onClick={handleClick}
    >
      <div className="d-flex align-items-center gap-2">
        <i className="bi bi-plus-circle" aria-hidden="true"></i>
        <span>{upperFirst(questionset.verbose_name)}</span>
      </div>
    </button>
  )
}

QuestionSetAddSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  setPrefix: PropTypes.string.isRequired,
}

export default QuestionSetAddSet
