import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { generateErrorMessageListItems } from './common/ErrorsListGroup'

import { ShowLink } from '../common/Links'

// Function to aggregate unique errors from elements
const aggregateUniqueErrors = (elements) => {
  const allErrors = elements.reduce((acc, element) => {
    return acc.concat(element.errors)
  }, [])

  // Filter out duplicate errors
  const uniqueErrors = [...new Set(allErrors)]

  return uniqueErrors
}

const ImportAggregatedErrorsPanel = ({ elements }) => {
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
    <div className="panel panel-danger panel-import-errors mt-10">
      <div className="panel-heading" onClick={updateShowErrors}>
        {errorsHeadingText}
        <div className="pull-right">
          <ShowLink show={showErrors} onClick={() => {}}/>
        </div>
      </div>
      {showErrors && (
        <ul className="list-group mb-5 pb-5 pt-5 pl-5 pr-5">
          {generateErrorMessageListItems(uniqueErrors)}
        </ul>
      )}
    </div>
  )
}

ImportAggregatedErrorsPanel.propTypes = {
  elements: PropTypes.array.isRequired
}

export default ImportAggregatedErrorsPanel
