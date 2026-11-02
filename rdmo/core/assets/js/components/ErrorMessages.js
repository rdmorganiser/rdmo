import React from 'react'
import { useSelector } from 'react-redux'

import { getErrorMessages } from '../utils/errors'

const ErrorMessages = () => {
  const errors = useSelector(state => state.errors)

  return Object.entries(errors).map(([key, error]) => {
    const messages = getErrorMessages(error)
    if (!messages.length) return null

    return (
      <div key={key} className="alert alert-danger" role="alert">
        <div className="fw-bold mb-1">
          {error.title || gettext('An error occurred.')}
        </div>
        {messages.map((message, index) => <div key={index}>{message}</div>)}
      </div>
    )
  })
}

export default ErrorMessages
