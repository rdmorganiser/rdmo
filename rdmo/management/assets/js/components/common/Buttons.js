import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const BackButton = ({ className }) => (
  <button className={classNames('element-button btn btn-sm btn-light border', className)}
          onClick={() => history.back()}>
    {gettext('Back')}
  </button>
)

BackButton.propTypes = {
  className: PropTypes.string
}

const SaveButton = ({ elementAction, onClick, disabled=false, back=false }) => {
  let text, className

  if (elementAction == 'create') {
    text = back ? gettext('Create') : gettext('Create and continue editing')
    className = classNames('btn btn-sm', {
      'btn-success': back,
      'btn-light border': !back
    })
  } else if (elementAction == 'copy') {
    text = back ? gettext('Copy') : gettext('Copy and continue editing')
    className = classNames('btn btn-sm', {
      'btn-info': back,
      'btn-light border': !back
    })
  } else {
    text = back ? gettext('Save') : gettext('Save and continue editing')
    className = classNames('btn btn-sm', {
      'btn-primary': back,
      'btn-light border': !back
    })
  }

  return (
    <button className={className} onClick={() => onClick(back)} disabled={disabled}>
      {text}
    </button>
  )
}

SaveButton.propTypes = {
  elementAction: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  back: PropTypes.bool
}

const NewButton = ({ onClick }) => (
  <button className="element-button btn btn-sm btn-success" onClick={() => onClick()}>
    {gettext('New')}
  </button>
)

NewButton.propTypes = {
  onClick: PropTypes.func.isRequired
}

const DeleteButton = ({ onClick, disabled=false }) => (
  <button className="element-button btn btn-sm btn-danger" onClick={() => onClick()} disabled={disabled}>
    {gettext('Delete')}
  </button>
)

DeleteButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

export { BackButton, SaveButton, NewButton, DeleteButton }
