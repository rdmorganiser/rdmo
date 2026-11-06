import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { generateWarningListItems } from './WarningsListGroup'

// Function to aggregate warnings from elements
const aggregateWarnings = (elements) => {
  return elements.reduce((acc, element) => {
    Object.entries(element.warnings).forEach(([uri, messages]) => {
      acc.push({ elementWarnings: { [uri]: messages }, elementModel: element.model, elementURI: element.uri })
    })
    return acc
  }, [])
}

const WarningsAggregated = ({ elements }) => {
  const [showWarnings, setShowWarnings] = useConfig('filter.import.warnings.show', false)

  const updateShowWarnings = () => setShowWarnings(!showWarnings)

  // Aggregate all warnings into a single list
  const aggregatedWarnings = aggregateWarnings(elements)

  const warningsHeadingText = <strong onClick={updateShowWarnings}>{gettext('Warnings')} ({elements.length}):</strong>

  return ( aggregatedWarnings.length > 0 && (
    <div className="card text-bg-warning mt-2">
      <div className="card-header cursor-pointer" onClick={updateShowWarnings}>
        <div className="d-flex align-items-center">
          <div className="flex-grow-1">
            {warningsHeadingText}
          </div>
          <span className={classNames('bi', {'bi-chevron-down': !showWarnings, 'bi-chevron-up': showWarnings})}></span>
        </div>
      </div>
      {
        showWarnings && (
          <ul className="list-group list-group-flush">
            {
              aggregatedWarnings.map(({ elementWarnings, elementModel, elementURI }) =>
                generateWarningListItems(elementWarnings, elementModel, elementURI)
              )
            }
          </ul>
        )
      }
    </div>
  )
  )
}

WarningsAggregated.propTypes = {
  elements: PropTypes.array.isRequired
}

export default WarningsAggregated
