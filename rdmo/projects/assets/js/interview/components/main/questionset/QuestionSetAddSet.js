import React from 'react'
import PropTypes from 'prop-types'
import { capitalize, maxBy } from 'lodash'

const QuestionSetAddSet = ({ questionset, sets, setPrefix, createSet }) => {
  const handleClick = () => {
    const lastSet = maxBy(sets, (s) => s.set_index)
    const setIndex = lastSet ? lastSet.set_index + 1 : 0

    createSet({
      set_prefix: setPrefix,
      set_index: setIndex
    })
  }

  return questionset.is_collection && (
    <button type="button" className="btn btn-success btn-add-set" onClick={handleClick}>
      <i className="fa fa-plus fa-btn"></i> {capitalize(questionset.verbose_name)}
    </button>
  )
}

QuestionSetAddSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  setPrefix: PropTypes.string.isRequired,
  createSet: PropTypes.func.isRequired
}

export default QuestionSetAddSet
