import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

// Helper function to generate error messages
const generateErrorMessageListItems = (messages, key) =>
  messages.map(message => <li className="text-danger error-item pb-5" key={key}>{message}</li>)

// Helper function to prepare the list of errors
export const prepareErrorsList = (errors) => {
  // Filter out duplicate errors
  const uniqueErrors = [...new Set(errors)]

  return uniqueErrors.map(message => (
    <ul className="list-unstyled error-list" key={uniqueId('error-list')}>
      {generateErrorMessageListItems([message], uniqueId('error-message'))}
    </ul>
  ))
}

const Errors = ({ element, showTitle = false }) => {
  const errorMessagesList = prepareErrorsList(element.errors)
  const show = element.errors.length > 0

  return show && (
    <div>
      {showTitle && (
        <div className="col-sm-12 mb-5 mt-5 text-danger">
          {gettext('Errors')}
        </div>
      )}
      <div className="mb-5 mt-5">
          {errorMessagesList}
      </div>
    </div>
  )
}

Errors.propTypes = {
  element: PropTypes.object.isRequired,
  showTitle: PropTypes.bool,
}

export default Errors
