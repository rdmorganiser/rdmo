import React from 'react'
import PropTypes from 'prop-types'

const BackButton = () => (
  <button className="element-button btn btn-xs btn-default" onClick={() => history.back()}>
    {gettext('Back')}
  </button>
)

const SaveButton = ({ elementAction, onClick, disabled=false, back=false }) => {
  let text, className = 'element-button btn btn-xs'
  if (elementAction == 'create') {
    text = back ? gettext('Create') : gettext('Create and continue editing')
    className += back ? ' btn-success' : ' btn-default'
  } else if (elementAction == 'copy') {
    text = back ? gettext('Copy') : gettext('Copy and continue editing')
    className += back ? ' btn-info' : ' btn-default'
  } else {
    text = back ? gettext('Save') : gettext('Save and continue editing')
    className += back ? ' btn-primary' : ' btn-default'
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
  <button className="element-button btn btn-xs btn-success" onClick={() => onClick()}>
    {gettext('New')}
  </button>
)

NewButton.propTypes = {
  onClick: PropTypes.func.isRequired
}

const DeleteButton = ({ onClick, disabled=false }) => (
  <button className="element-button btn btn-xs btn-danger" onClick={() => onClick()} disabled={disabled}>
    {gettext('Delete')}
  </button>
)

DeleteButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
}

export { BackButton, SaveButton, NewButton, DeleteButton }
