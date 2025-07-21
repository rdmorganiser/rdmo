// Errors.js
import React from 'react'
import PropTypes from 'prop-types'
import ErrorsListGroup from './ErrorsListGroup'
import isUndefined from 'lodash/isUndefined'

const Errors = ({ elementErrors }) => {
  const show = !isUndefined(elementErrors) &&  elementErrors.length > 0
  const errorsHeadingText = <strong>{gettext('Errors')}</strong>

  return show && (
    <div className="panel panel-danger mt-10 mb-0">
      <div className="panel-heading">{errorsHeadingText}</div>
      <ErrorsListGroup elementErrors={elementErrors} />
    </div>
  )
}

Errors.propTypes = {
  elementErrors: PropTypes.array.isRequired,
}

export default Errors
