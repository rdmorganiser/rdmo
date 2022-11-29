import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Errors = ({ config, errors }) => {
  return (
    <div className="errors">
      <div className="panel panel-default">
        <div className="panel-body text-danger">
          <p>
            <strong>{gettext('One or more errors occured:')}</strong>
          </p>
          <ul className="mb-0">
            { errors.map((error, index) => <li key={index}>{error}</li>) }
          </ul>
        </div>
      </div>
    </div>
  )
}

Errors.propTypes = {
  value: PropTypes.string,
  onChange: PropTypes.func
}

export default Errors
