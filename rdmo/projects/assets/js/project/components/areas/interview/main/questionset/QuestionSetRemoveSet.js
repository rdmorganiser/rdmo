import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { LinkButton, Modal } from 'rdmo/core/assets/js/components'
import useModal from 'rdmo/core/assets/js/hooks/useModal'
import { selectReadOnly } from 'rdmo/projects/assets/js/common/selectors/permissions'

import { deleteSet } from '../../../../../actions/interviewActions'

const QuestionRemoveSet = ({ questionset, currentSet }) => {
  const dispatch = useDispatch()
  const readOnly = useSelector(selectReadOnly)
  const modal = useModal()
  const title = gettext('Remove block')

  const handleRemoveSet = () => {
    dispatch(deleteSet(currentSet))
    modal.close()
  }

  return !readOnly && questionset.is_collection && (
    <>
      <LinkButton
        className="btn btn-link btn-remove-set"
        title={title}
        aria-label={title}
        onClick={modal.open}
      >
        <i className="bi bi-x-circle" aria-hidden="true"></i>
      </LinkButton>

      <Modal
        title={gettext('Remove block')} show={modal.show} submitLabel={gettext('Remove')}
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
}

export default QuestionRemoveSet
