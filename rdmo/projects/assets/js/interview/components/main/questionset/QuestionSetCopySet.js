import React from 'react'
import PropTypes from 'prop-types'
import { last } from 'lodash'

import Modal from 'rdmo/core/assets/js/components/Modal'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

const QuestionCopySet = ({ questionset, sets, currentSet, copySet }) => {

  const modal = useModal()

  const handleCopySet = () => {
    copySet(currentSet, null, {
      set_prefix: currentSet.set_prefix,
      set_index: last(sets) ? last(sets).set_index + 1 : 0,
    })
    modal.close()
  }

  return questionset.is_collection && (
    <>
      <button type="button" className="btn btn-link btn-copy-set" onClick={modal.open}>
        <i className="fa fa-copy fa-btn"></i>
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
  copySet: PropTypes.func.isRequired
}

export default QuestionCopySet
