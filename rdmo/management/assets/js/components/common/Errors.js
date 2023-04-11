import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isString from 'lodash/isString'

const ElementErrors = ({ element }) => {
  if (element.errors) {
    const errorList = Object.values(element.errors).flat().reduce((acc, cur) => {
      if (isString(cur)) {
        acc.push(cur)
      } else {
        Object.values(cur).forEach(value => {
          acc = acc.concat(value)
        })
      }

      return acc
    }, [])

    return element.errors && (
      <ul className="list-unstyled text-danger mb-0">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>
    )
  } else {
    return null
  }



}

ElementErrors.propTypes = {
  element: PropTypes.object.isRequired
}

export { ElementErrors }
