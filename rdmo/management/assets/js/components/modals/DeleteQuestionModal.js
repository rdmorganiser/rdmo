import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteQuestionModal = ({ question, pages, questionsets, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete question')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the question:')}
    </p>
    <p>
      <code className="code-questions">{question.uri}</code>
    </p>
    {
      pages.length > 0 && <>
        <p>
          {gettext('This question is used in the following pages, from which it will be removed:')}
        </p>
        {
          pages.map((page, index) => (
            <p key={index}>
              <code className="code-questions">{page.uri}</code>
            </p>
          ))
        }
      </>
    }
    {
      questionsets.length > 0 && <>
        <p>
          {gettext('This question is used in the following question sets, from which it will be removed:')}
        </p>
        {
          questionsets.map((questionset, index) => (
            <p key={index}>
              <code className="code-questions">{questionset.uri}</code>
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

DeleteQuestionModal.propTypes = {
  question: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  questionsets: PropTypes.array.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteQuestionModal
