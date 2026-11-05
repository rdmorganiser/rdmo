import React from 'react'
import { useSelector } from 'react-redux'

import { getErrorMessages } from '../utils/errors'

const Errors = () => {
  const errors = useSelector(state => state.errors)

  const messages = Object.entries(errors).flatMap(([key, error]) => (
    getErrorMessages(error).map((message, index) => (
      <li key={`${key}/${index}`}>
        {error.title && <strong>{error.title}: </strong>}
        {message}
      </li>
    ))
  ))

  if (!messages.length) return null

  return (
    <div className="errors alert alert-danger" role="alert">
      <h1>{gettext('Error!')}</h1>
      <ul>{messages}</ul>
    </div>
  )
}

export default Errors
