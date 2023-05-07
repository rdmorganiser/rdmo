import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'

const BackButton = () => (
  <button className="element-button btn btn-xs btn-default" onClick={event => history.back()}>
    {gettext('Back')}
  </button>
)

const SaveButton = ({ element, elementAction, onClick, back }) => {
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
    <button className={className} onClick={event => onClick(back)}>
      {text}
    </button>
  )
}

SaveButton.propTypes = {
  element: PropTypes.object.isRequired,
  elementAction: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  back: PropTypes.bool
}

const NewButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-success" onClick={event => onClick()}>
    {gettext('New')}
  </button>
)

NewButton.propTypes = {
  onClick: PropTypes.func.isRequired
}

const DeleteButton = ({ element, onClick }) => {
  return element.id && (
    <button className="element-button btn btn-xs btn-danger" onClick={event => onClick()}>
      {gettext('Delete')}
    </button>
  )
}

DeleteButton.propTypes = {
  element: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}

export { BackButton, SaveButton, NewButton, DeleteButton }
