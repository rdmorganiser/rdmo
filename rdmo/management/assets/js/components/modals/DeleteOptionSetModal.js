import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteOptionSetModal = ({ optionset, questions, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete option set')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the option set:')}
    </p>
    <p>
      <code className="code-options">{optionset.uri}</code>
    </p>
    {
      questions.length > 0 && <>
        <p>
          {gettext('This option set is used in the following questions, from which it will be removed:')}
        </p>
        {
          questions.map((question, index) => (
            <p key={index}>
              <code className="code-questions">{question.uri}</code>
            </p>
          ))
        }
      </>
    }
    <p className="text-danger">
      {gettext('This action cannot be undone!')}
    </p>
  </DeleteElementModal>
)

DeleteOptionSetModal.propTypes = {
  optionset: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteOptionSetModal
