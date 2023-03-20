import React, { Component} from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

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
  onClick: PropTypes.func
}

const NewButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-success" onClick={event => onClick()}>
    {gettext('New')}
  </button>
)

NewButton.propTypes = {
  onClick: PropTypes.func
}

const DeleteButton = ({ onClick }) => (
  <button className="element-button btn btn-xs btn-danger" onClick={event => onClick()}>
    {gettext('Delete')}
  </button>
)

DeleteButton.propTypes = {
  onClick: PropTypes.func
}

export { BackButton, NewButton, SaveButton, DeleteButton }
