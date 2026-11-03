import React from 'react'
import { useSelector } from 'react-redux'

import { getErrorMessages } from '../utils/errors'

const Errors = () => {
  const errors = useSelector(state => state.errors)

  const messages = Object.entries(errors).flatMap(([key, error]) => (
    getErrorMessages(error).map((message, index) => (
      <li key={`${key}/${index}`} className="alert alert-danger" role="alert">
        {error.title && <strong>{error.title}: </strong>}
        {message}
      </li>
    ))
  ))

  if (!messages.length) return null

  return (
    <div className="errors">
      <h1 className="mb-5">{gettext('Error!')}</h1>
      <ul className="list-unstyled">{messages}</ul>
    </div>
  )
}

export default Errors
