import React from 'react'
import PropTypes from 'prop-types'
import { isNil } from 'lodash'

const getMessage = (error) => {
  if (error.constructor.name === 'ValidationError') {
    if (error.errors.conflict) {
      return gettext('This field could not be saved, since somebody else did so while you were editing.' +
                     ' You will need to reload the page to make changes, but your input will be overwritten.')
    } else if (error.errors.quota) {
       return gettext('You reached the file quota for this project.')
    }
  } else if (error.constructor.name === 'ApiError') {
    if (error.status === 404) {
      return gettext('This field could not be saved, since somebody else removed it while you were editing.' +
                     ' You will need to reload the page to proceed, but your input will be lost.')
    } else {
      return error.errors.api
    }
  } else {
    return gettext('An unknown error occured, please contact support')
  }
}

const QuestionError = ({ value }) => {
  return !isNil(value) && !isNil(value.error) && (
    <ul className="help-block list-unstyled">
      <li className="text-danger">{getMessage(value.error)}</li>
    </ul>
  )
}

QuestionError.propTypes = {
  value: PropTypes.object
}

export default QuestionError
