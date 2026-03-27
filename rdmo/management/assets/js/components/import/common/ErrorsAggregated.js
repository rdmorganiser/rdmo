import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { generateErrorMessageListItems } from './ErrorsListGroup'

// Function to aggregate unique errors from elements
const aggregateUniqueErrors = (elements) => {
  const allErrors = elements.reduce((acc, element) => {
    return acc.concat(element.errors)
  }, [])

  // Filter out duplicate errors
  const uniqueErrors = [...new Set(allErrors)]

  return uniqueErrors
}

const ErrorsAggregated = ({ elements }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateShowErrors = () => {
    const currentVal = isTruthy(get(config, 'filter.import.errors.show', false))
    dispatch(updateConfig('filter.import.errors.show', !currentVal))
  }

  const showErrors = isTruthy(get(config, 'filter.import.errors.show', false))

  // Aggregate all unique errors into a single flat array
  const uniqueErrors = aggregateUniqueErrors(elements)

  const errorsHeadingText = <strong onClick={updateShowErrors}>{gettext('Errors')} ({elements.length}) :</strong>

  return ( uniqueErrors.length > 0 &&
    <div className="card text-bg-danger mt-2">
      <div className="card-header cursor-pointer" onClick={updateShowErrors}>
        <div className="d-flex align-items-center">
          <div className="flex-grow-1">
            {errorsHeadingText}
          </div>
          <span className={classNames('bi', {'bi-chevron-down': !showErrors, 'bi-chevron-up': showErrors})}></span>
        </div>
      </div>
      {
        showErrors && (
          <ul className="list-group list-group-flush">
            {generateErrorMessageListItems(uniqueErrors)}
          </ul>
        )
      }
    </div>
  )
}

ErrorsAggregated.propTypes = {
  elements: PropTypes.array.isRequired
}

export default ErrorsAggregated
