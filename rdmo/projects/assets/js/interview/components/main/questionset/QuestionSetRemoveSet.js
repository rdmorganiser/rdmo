import React from 'react'
import PropTypes from 'prop-types'
import { capitalize } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import QuestionSetDeleteModal from './QuestionSetDeleteModal'

const QuestionRemoveSet = ({ questionset, currentSet, deleteSet }) => {

  const modal = useModal()

  const handleDeleteSet = () => {
    deleteSet(currentSet)
    modal.close()
  }

  return questionset.is_collection && (
    <>
      <button type="button" className="btn btn-link btn-remove-set" onClick={modal.open}>
        <i className="fa fa-times fa-btn"></i>
      </button>

      <QuestionSetDeleteModal
        title={capitalize(questionset.verbose_name)}
        show={modal.show}
        onClose={modal.close}
        onSubmit={handleDeleteSet}
      />
    </>
  )
}

QuestionRemoveSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  currentSet: PropTypes.object.isRequired,
  deleteSet: PropTypes.func.isRequired
}

export default QuestionRemoveSet
