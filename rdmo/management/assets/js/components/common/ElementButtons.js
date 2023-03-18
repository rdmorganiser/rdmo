import React, { Component} from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

const ElementButtons = ({ onCreate, onSave }) => {
  return (
    <div className="element-buttons">
      <button className="btn btn-xs btn-default" onClick={event => history.back()}>
        {gettext('Back')}
      </button>
      {
        !isUndefined(onCreate) &&
        <button className="btn btn-xs btn-success" onClick={event => onCreate()}>
          {gettext('New')}
        </button>
      }
      {
        !isUndefined(onSave) &&
        <button className="btn btn-xs btn-primary" onClick={event => onSave()}>
          {gettext('Save')}
        </button>
      }
    </div>
  )
}

ElementButtons.propTypes = {
  onSave: PropTypes.func
}

export default ElementButtons
