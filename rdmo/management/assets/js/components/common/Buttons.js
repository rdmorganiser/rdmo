import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'

const BackButton = () => (
  <button className="element-button btn btn-xs btn-default" onClick={event => history.back()}>
    {gettext('Back')}
  </button>
)

const SaveButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-primary" onClick={event => onClick()}>
    {gettext('Save')}
  </button>
)

SaveButton.propTypes = {
  onClick: PropTypes.func.isRequired
}

const CreateButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-success" onClick={event => onClick()}>
    {gettext('Create')}
  </button>
)

CreateButton.propTypes = {
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

const DeleteButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-danger" onClick={event => onClick()}>
    {gettext('Delete')}
  </button>
)

DeleteButton.propTypes = {
  onClick: PropTypes.func.isRequired
}

export { BackButton, SaveButton, CreateButton, NewButton, DeleteButton }
