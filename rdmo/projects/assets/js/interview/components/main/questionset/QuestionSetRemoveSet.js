import React from 'react'
import PropTypes from 'prop-types'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import Modal from 'rdmo/core/assets/js/components/Modal'

const QuestionRemoveSet = ({ questionset, currentSet, disabled, deleteSet }) => {

  const modal = useModal()

  const handleRemoveSet = () => {
    deleteSet(currentSet)
    modal.close()
  }

  return !disabled && questionset.is_collection && (
    <>
      <button type="button" className="btn btn-link btn-remove-set" onClick={modal.open}>
        <i className="fa fa-times fa-btn"></i>
      </button>

      <Modal title={gettext('Remove block')} show={modal.show} submitLabel={gettext('Remove')}
             submitProps={{className: 'btn btn-danger'}}
             onClose={modal.close} onSubmit={handleRemoveSet}>
        <p>{gettext('You are about to permanently remove this block.')}</p>
        <p className="text-danger">{gettext('This action cannot be undone!')}</p>
      </Modal>
    </>
  )
}

QuestionRemoveSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  currentSet: PropTypes.object.isRequired,
  disabled: PropTypes.bool.isRequired,
  deleteSet: PropTypes.func.isRequired
}

export default QuestionRemoveSet
