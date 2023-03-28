import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'

const BackButton = () => (
  <button className="element-button btn btn-xs btn-default" onClick={event => history.back()}>
    {gettext('Back')}
  </button>
)

const SaveButton = ({ element, onClick, back }) => {

  const className = classNames({
    'element-button btn btn-xs': true,
    'btn-primary': back,
    'btn-default': !back
  })

  return (
    <button className={className} onClick={event => onClick(back)}>
      {back ? gettext('Save') : gettext('Save and continue editing')}
    </button>
  )
}

SaveButton.propTypes = {
  onClick: PropTypes.func.isRequired
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
  onClick: PropTypes.func.isRequired
}

export { BackButton, SaveButton, NewButton, DeleteButton }
