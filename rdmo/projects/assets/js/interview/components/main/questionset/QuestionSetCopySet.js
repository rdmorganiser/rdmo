import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import { generateSetIndex } from '../../../utils/set'

const QuestionCopySet = ({ questionset, sets, currentSet, disabled, copySet }) => {

  const modal = useModal()

  const handleCopySet = () => {
    copySet(currentSet, null, {
      set_prefix: currentSet.set_prefix,
      set_index: generateSetIndex(sets, currentSet),
      element: questionset
    })
    modal.close()
  }

  return !disabled && questionset.is_collection && (
    <>
      <button type="button" className="btn btn-link btn-copy-set"
              title={'Copy block'} aria-label={'Copy block'}
              onClick={modal.open}>
        <i className="fa fa-copy fa-btn" aria-hidden="true"></i>
      </button>

      <Modal title={gettext('Copy block')} show={modal.show} submitLabel={gettext('Copy')}
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
  disabled: PropTypes.bool.isRequired,
  copySet: PropTypes.func.isRequired
}

export default QuestionCopySet
