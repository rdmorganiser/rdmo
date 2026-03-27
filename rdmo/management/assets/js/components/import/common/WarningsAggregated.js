import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

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
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateShowWarnings = () => {
    const currentVal = isTruthy(get(config, 'filter.import.warnings.show', false))
    dispatch(updateConfig('filter.import.warnings.show', !currentVal))
  }

  const showWarnings = isTruthy(get(config, 'filter.import.warnings.show', false))

  // Aggregate all warnings into a single list
  const aggregatedWarnings = aggregateWarnings(elements)

  const warningsHeadingText = <strong onClick={updateShowWarnings}>{gettext('Warnings')} ({elements.length}):</strong>

  return ( aggregatedWarnings.length > 0 &&
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
}

WarningsAggregated.propTypes = {
  elements: PropTypes.array.isRequired
}

export default WarningsAggregated
