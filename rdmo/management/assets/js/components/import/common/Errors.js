import React from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import ErrorsListGroup from './ErrorsListGroup'

const Errors = ({ elementErrors }) => {
  const show = !isUndefined(elementErrors) &&  elementErrors.length > 0
  const errorsHeadingText = <strong>{gettext('Errors')}</strong>

  return show && (
    <div className="card text-bg-danger my-2">
      <div className="card-header">{errorsHeadingText}</div>
      <ErrorsListGroup elementErrors={elementErrors} />
    </div>
  )
}

Errors.propTypes = {
  elementErrors: PropTypes.array.isRequired,
}

export default Errors
