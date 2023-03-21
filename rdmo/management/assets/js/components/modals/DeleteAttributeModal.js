import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteAttributeModal = ({ attribute, attributes, conditions, pages, questionsets, questions, tasks,
                                show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete attribute')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the attribute:')}
    </p>
    <p>
      <code className="code-domain">{attribute.uri}</code>
    </p>
    {
      (attribute.values_count > 0 || attribute.project_count > 0) &&
          <p dangerouslySetInnerHTML={{
      __html: interpolate(ngettext(
        'This attribute is used for <b>%s values</b> in <b>one project</b>.',
        'This attribute is used for <b>%s values</b> in <b>%s projects</b>.',
        attribute.projects_count
      ), [attribute.values_count, attribute.projects_count])}} />
    }
    {
      attributes.length > 0 && <>
        <p>
          {gettext('This following attributes are descendants of this attribute and will be removed as well:')}
        </p>
        {
          attributes.map((attribute, index) => (
            <p key={index}>
              <code className="code-domain">{attribute.uri}</code>
            </p>
          ))
        }
      </>
    }
    {
      pages.length > 0 && <>
        <p>
          {gettext('This attribute is used in the following pages, from which it will be removed:')}
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
          {gettext('This attribute is used in the following question sets, from which it will be removed:')}
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
          {gettext('This attribute is used in the following questions, from which it will be removed:')}
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
          {gettext('This attribute is used in the following tasks, from which it will be removed:')}
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

DeleteAttributeModal.propTypes = {
  attribute: PropTypes.object.isRequired,
  conditions: PropTypes.array.isRequired,
  pages: PropTypes.array.isRequired,
  questionsets: PropTypes.array.isRequired,
  questions: PropTypes.array.isRequired,
  tasks: PropTypes.array.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteAttributeModal
