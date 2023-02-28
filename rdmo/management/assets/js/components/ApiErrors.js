import React, { Component} from 'react'
import PropTypes from 'prop-types'

const ApiErrors = ({ errors }) => {
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

ApiErrors.propTypes = {
  errors: PropTypes.array
}

export default ApiErrors
