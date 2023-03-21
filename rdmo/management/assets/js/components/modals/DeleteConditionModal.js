import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteConditionModal = ({ condition, optionsets, pages, questionsets, questions, tasks,
                                show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete condition')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the condition:')}
    </p>
    <p>
      <code className="code-conditions">{condition.uri}</code>
    </p>
    {
      optionsets.length > 0 && <>
        <p>
          {gettext('This condition is used in the following option sets, from which it will be removed:')}
        </p>
        {
          optionsets.map((optionset, index) => (
            <p key={index}>
              <code className="code-options">{optionset.uri}</code>
            </p>
          ))
        }
      </>
    }
    {
      pages.length > 0 && <>
        <p>
          {gettext('This condition is used in the following pages, from which it will be removed:')}
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
          {gettext('This condition is used in the following question sets, from which it will be removed:')}
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
    {
      questions.length > 0 && <>
        <p>
          {gettext('This condition is used in the following questions, from which it will be removed:')}
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
    {
      tasks.length > 0 && <>
        <p>
          {gettext('This condition is used in the following tasks, from which it will be removed:')}
        </p>
        {
          tasks.map((task, index) => (
            <p key={index}>
              <code className="code-tasks">{task.uri}</code>
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

DeleteConditionModal.propTypes = {
  condition: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteConditionModal
