import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty, isString } from 'lodash'

const MainErrors = ({ errors }) => {
  return (
    <div className="errors">
      <div className="panel panel-default">
        <div className="panel-body text-danger">
          <p>
            <strong>{gettext('One or more errors occurred:')}</strong>
          </p>
          <ul className="mb-0">
            {errors.map((error, index) => <li key={index}>{error}</li>)}
          </ul>
        </div>
      </div>
    </div>
  )
}

MainErrors.propTypes = {
  errors: PropTypes.array
}

const ElementErrors = ({ element }) => {
  if (!isEmpty(element.errors)) {
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

    return (
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

export { ElementErrors, MainErrors }
