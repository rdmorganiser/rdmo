import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import isEmpty from 'lodash/isEmpty'

// Helper function to generate error messages
const generateErrorMessages = (messages, key) =>
  messages.map(message => <li className="text-danger" key={key}>{message}</li>)

// Helper function to prepare the list of errors
const prepareErrorsList = (errors) => {
  // Filter out duplicate errors
  const uniqueErrors = [...new Set(errors)]

  return uniqueErrors.map(message => (
    <ul className="list-unstyled" key={uniqueId('error-list')}>
      {generateErrorMessages([message], uniqueId('error-message'))}
    </ul>
  ))
}

const Errors = ({ element, showTitle = false }) => {
  const listErrorMessages = prepareErrorsList(element.errors)

  return !isEmpty(element.errors) && (
    <div className="row text-danger mt-10">
      {showTitle && (
        <div className="col-sm-3 text-right">
          {gettext('Errors')}
        </div>
      )}
      <div className={`col-sm-${showTitle ? 9 : 12}`}>
        <ul className="list-unstyled">
          {listErrorMessages}
        </ul>
      </div>
    </div>
  )
}

Errors.propTypes = {
  element: PropTypes.object.isRequired,
  showTitle: PropTypes.bool,
}

export default Errors
