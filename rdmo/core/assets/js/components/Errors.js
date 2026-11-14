import React from 'react'
import { useSelector } from 'react-redux'

import Template from 'rdmo/core/assets/js/components/Template'

import { getErrorMessages } from '../utils/errors'

const Errors = () => {
  const errors = useSelector(state => state.errors)

  const messages = Object.entries(errors).flatMap(([key, error]) => (
    getErrorMessages(error).map((message, index) => (
      <li key={`${key}/${index}`} >
        {error.title && <strong>{error.title}: </strong>}
        {message}
      </li>
    ))
  ))

  if (!messages.length) return null

  return (
    <div className="errors alert alert-danger mb-5" role="alert">
      <h2>{gettext('Error!')}</h2>
      <Template template="errors_help" />
      <ul className="list-unstyled">{messages}</ul>
      <button className="d-block btn btn-danger" onClick={() => window.location.reload()}>
        {gettext('Reload page')}
      </button>
    </div>
  )
}

export default Errors
