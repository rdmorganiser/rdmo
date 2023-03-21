import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'

import { DeleteElementModal } from '../common/ElementModals'

const DeleteOptionModal = ({ option, conditions, show, onClose, onDelete }) => (
  <DeleteElementModal title={gettext('Delete option')} show={show} onClose={onClose} onDelete={onDelete}>
    <p>
      {gettext('You are about to permanently delete the option:')}
    </p>
    <p>
      <code className="code-options">{option.uri}</code>
    </p>
    {
      (option.values_count > 0 || option.project_count > 0) &&
          <p dangerouslySetInnerHTML={{
      __html: interpolate(ngettext(
        'This option is used for <b>%s values</b> in <b>one project</b>.',
        'This option is used for <b>%s values</b> in <b>%s projects</b>.',
        option.projects_count
      ), [option.values_count, option.projects_count])}} />
    }
    {
      conditions.length > 0 && <>
        <p>
          {gettext('This option is used in the following condition, which will not be usable afterwards:')}
        </p>
        {
          conditions.map((condition, index) => (
            <p key={index}>
              <code className="code-conditions">{condition.uri}</code>
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

DeleteOptionModal.propTypes = {
  option: PropTypes.object.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeleteOptionModal
