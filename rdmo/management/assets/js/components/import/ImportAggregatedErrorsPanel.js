// ImportAggregatedErrorsPanel.js
import React from 'react'
import PropTypes from 'prop-types'
import { ShowLink } from '../common/Links'
import { generateErrorMessageListItems } from './common/ErrorsListGroup'
import get from 'lodash/get'

// Function to aggregate unique errors from elements
const aggregateUniqueErrors = (elements) => {
  const allErrors = elements.reduce((acc, element) => {
    return acc.concat(element.errors)
  }, [])

  // Filter out duplicate errors
  const uniqueErrors = [...new Set(allErrors)]

  return uniqueErrors
}

const ImportAggregatedErrorsPanel = ({ config, elements, configActions }) => {
  const updateShowErrors = () => {
    const currentVal = get(config, 'filter.import.errors.show', false)
    configActions.updateConfig('filter.import.errors.show', !currentVal)
  }

  const showErrors = get(config, 'filter.import.errors.show', false)

  // Aggregate all unique errors into a single flat array
  const uniqueErrors = aggregateUniqueErrors(elements)

  const errorsHeadingText = <strong onClick={updateShowErrors}>{gettext('Errors')} ({elements.length}) :</strong>

  return (
    <div className="panel panel-danger mt-5">
      <div className="panel-heading">{errorsHeadingText}
        <div className="pull-right">
          <ShowLink show={showErrors} onClick={updateShowErrors}/>
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
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired
}

export default ImportAggregatedErrorsPanel
