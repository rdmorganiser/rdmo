import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const ErrorList = ({ errors }) => (
  !isEmpty(errors) && (
    <div className="invalid-feedback">
      {errors.map((error, index) => <div key={index} className="mb-1">{error}</div>)}
    </div>
  )
)

ErrorList.propTypes = {
  errors: PropTypes.array
}

export default ErrorList
