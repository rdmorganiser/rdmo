import React from 'react'
import PropTypes from 'prop-types'
import { capitalize } from 'lodash'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import QuestionSetDeleteModal from './QuestionSetDeleteModal'

const QuestionAddSet = ({ questionset, set, deleteSet }) => {

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useModal()

  const handleDeleteSet = () => {
    deleteSet(set)
    closeDeleteModal()
  }

  return (
    <>
      <button type="button" className="btn btn-link btn-remove-set" onClick={openDeleteModal}>
        <i className="fa fa-times fa-btn"></i>
      </button>

      <QuestionSetDeleteModal
        title={capitalize(questionset.verbose_name)}
        show={showDeleteModal}
        onClose={closeDeleteModal}
        onSubmit={handleDeleteSet}
      />
    </>
  )
}

QuestionAddSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  set: PropTypes.object.isRequired,
  deleteSet: PropTypes.func.isRequired
}

export default QuestionAddSet
