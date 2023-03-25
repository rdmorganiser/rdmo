import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'


const ElementErrors = ({ element }) => {
  return element.errors && (
    <ul className="list-unstyled text-danger mb-0">
      {Object.values(element.errors).flat().map((error, index) => <li key={index}>{error}</li>)}
    </ul>
  )
}

ElementErrors.propTypes = {
  element: PropTypes.object.isRequired
}

export { ElementErrors }
