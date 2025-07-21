// ErrorsListGroup.js
import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

// Helper function to generate error messages
export const generateErrorMessageListItems = (messages) =>
  messages.map(message => (
    <li className="list-group-item text-danger" key={uniqueId('error-message')}>
      <div className="text-danger">
        {message}
      </div>
    </li>
  ))

const ErrorsListGroup = ({ elementErrors }) => {
  // Filter out duplicate elementErrors
  const uniqueErrors = [...new Set(elementErrors)]

  return (
    <ul className="list-group">
      {generateErrorMessageListItems(uniqueErrors)}
    </ul>
  )
}

ErrorsListGroup.propTypes = {
  elementErrors: PropTypes.array.isRequired
}

export default ErrorsListGroup
