import React from 'react'
import PropTypes from 'prop-types'
import { capitalize, last } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import QuestionSetCopyModal from './QuestionSetCopyModal'

const QuestionCopySet = ({ questionset, sets, currentSet, copySet }) => {

  const [showCopyModal, openCopyModal, closeCopyModal] = useModal()

  const handleCopySet = () => {
    copySet(currentSet, null, {
      set_prefix: currentSet.set_prefix,
      set_index: last(sets) ? last(sets).set_index + 1 : 0,
    })
    closeCopyModal()
  }

  return questionset.is_collection && (
    <>
      <button type="button" className="btn btn-link btn-copy-set" onClick={openCopyModal}>
        <i className="fa fa-copy fa-btn"></i>
      </button>

      <QuestionSetCopyModal
        title={capitalize(questionset.verbose_name)}
        show={showCopyModal}
        onClose={closeCopyModal}
        onSubmit={handleCopySet}
      />
    </>
  )
}

QuestionCopySet.propTypes = {
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired,
  copySet: PropTypes.func.isRequired
}

export default QuestionCopySet
