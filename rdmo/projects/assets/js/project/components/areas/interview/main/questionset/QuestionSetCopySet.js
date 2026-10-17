import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { LinkButton, Modal } from 'rdmo/core/assets/js/components'
import useModal from 'rdmo/core/assets/js/hooks/useModal'

import { copySet } from '../../../../../actions/interviewActions'
import { useReadOnly } from '../../../../../hooks'
import { generateSetIndex } from '../../../../../utils/set'

const QuestionCopySet = ({ questionset, sets, currentSet }) => {
  const dispatch = useDispatch()
  const modal = useModal()
  const readOnly = useReadOnly()
  const title = gettext('Copy block')

  const handleCopySet = () => {
    dispatch(copySet(currentSet, null, {
      set_prefix: currentSet.set_prefix,
      set_index: generateSetIndex(sets, currentSet),
      element: questionset
    }))
    modal.close()
  }

  return !readOnly && questionset.is_collection && (
    <>
      <LinkButton
        className="copy-set-button"
        title={title}
        aria-label={title}
        onClick={modal.open}
      >
        <i className="bi bi-copy" aria-hidden="true"></i>
      </LinkButton>

      <Modal
        title={gettext('Copy block')} show={modal.show} submitLabel={gettext('Copy')}
        submitProps={{className: 'btn btn-info'}}
        onClose={modal.close} onSubmit={handleCopySet}>
      </Modal>
    </>
  )
}

QuestionCopySet.propTypes = {
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired,
}

export default QuestionCopySet
